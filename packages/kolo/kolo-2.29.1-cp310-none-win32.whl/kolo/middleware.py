from __future__ import annotations

import contextlib
import datetime
import inspect
import json
import logging
import mimetypes
import os
import sys
import threading
from hashlib import sha1
from itertools import chain
from pathlib import Path
from typing import Awaitable, Callable, List

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.conf import settings
from django.core.servers.basehttp import ServerHandler
from django.http import (
    FileResponse,
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    JsonResponse,
)
from django.utils.cache import patch_response_headers
from django.utils.dateparse import parse_datetime
from django.utils.http import http_date
from django.views.decorators.cache import cache_control
from django.views.decorators.http import condition, conditional_page

from .checks import get_third_party_profiler
from .config import create_kolo_directory, load_config
from .db import get_db_last_modified, setup_db
from .profiler import KoloProfiler
from .serialize import monkeypatch_queryset_repr
from .web.home import kolo_web_home

logger = logging.getLogger("kolo")

DjangoView = Callable[[HttpRequest], HttpResponse]
DjangoAsyncView = Callable[[HttpRequest], Awaitable[HttpResponse]]


class KoloMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(self, get_response: DjangoView | DjangoAsyncView) -> None:
        self._is_coroutine = iscoroutinefunction(get_response)
        if self._is_coroutine:
            markcoroutinefunction(self)
        self._get_response = get_response
        self.config = load_config()
        self.upload_token = self.get_upload_token()
        self.enabled = self.should_enable()
        if self.enabled:
            self.db_path = setup_db()

            # TODO: Put the full URL here not just the /_kolo/ path
            if self.config.get("web_experience", False):
                print("\nView recent requests at /_kolo/")

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if self._is_coroutine:
            # TODO: Handle _kolo/ for asgi???
            get_response = self.aget_response
        else:
            if request.path.startswith("/_kolo"):
                return kolo_web_router(request)

            get_response = self.get_response  # type: ignore

        # WARNING: Because Django's runserver uses threading, we need
        # to be careful about thread safety here.
        if not self.enabled or self.check_for_third_party_profiler():
            return get_response(request)  # type: ignore

        filter_config = self.config.get("filters", {})
        ignore_request_paths = filter_config.get("ignore_request_paths", [])
        for path in ignore_request_paths:
            if path in request.path:
                return get_response(request)  # type: ignore

        # Don't store the KoloProfiler on self to avoid threadsafety
        # bugs. If a different thread gets this instance of KoloProfiler
        # at the wrong time, we lose the original profiler's trace.
        profiler = KoloProfiler(
            self.db_path, config=self.config, source="kolo.middleware.KoloMiddleware"
        )

        monkeypatch_queryset_repr()
        if self._is_coroutine:
            return self.aprofile_response(request, profiler)
        else:
            return self.profile_response(request, profiler)

    def profile_response(self, request, profiler):
        with profiler:
            response = self.get_response(request)
        self.save_trace(profiler)
        return response

    async def aprofile_response(self, request, profiler):
        with profiler:
            response = await self.aget_response(request)
        self.save_trace(profiler)
        return response

    async def aget_response(self, request: HttpRequest) -> HttpResponse:
        response = await self._get_response(request)  # type: ignore
        return response

    def get_response(self, request: HttpRequest) -> HttpResponse:
        response = self._get_response(request)
        return response  # type: ignore

    def save_trace(self, profiler):
        if settings.DEBUG is False and self.upload_token:
            profiler.upload_trace_in_thread(self.upload_token)
        else:
            profiler.save_trace_in_thread()

    def check_for_third_party_profiler(self) -> bool:
        profiler = get_third_party_profiler(self.config)
        if profiler:
            logger.warning("Profiler %s is active, disabling KoloMiddleware", profiler)
            return True
        return False

    def should_enable(self) -> bool:
        if settings.DEBUG is False and self.upload_token is None:
            logger.debug("DEBUG mode is off, disabling KoloMiddleware")
            return False

        if os.environ.get("KOLO_DISABLE", "false").lower() not in ["false", "0"]:
            logger.debug("KOLO_DISABLE is set, disabling KoloMiddleware")
            return False

        return not self.check_for_third_party_profiler()

    def get_upload_token(self):
        if not self.config.get("production_beta", False):
            return None

        upload_token = os.environ.get("KOLO_API_TOKEN", None)
        if upload_token is None:
            logging.warning(
                "Kolo production beta is enabled, but `KOLO_API_TOKEN` environment variable is not set."
            )
            return None

        if upload_token.startswith("kolo_prod_"):
            return upload_token

        logging.warning("`KOLO_API_TOKEN` is invalid.")
        return None


@contextlib.contextmanager
def hide_from_runserver(*args, **kwds):
    """
    Hides the requestline log messages from runserver's stdout.
    This works because Django's runserver is built on `wsgiref` which is ultimately built on `TCPServer` and the notion
    of a "server" creating a class "per request" which means we can rely on there being one `WSGIRequestHandler`
    for every incoming request, and we can modify that instance's methods to silence it.

    We don't want to restore the original method on exiting the context manager, because that would be "too soon" and
    the log message would ultimately still get spooled out at the WSGI server layer later (i.e. higher up the callstack)
    """
    using_reloader = os.environ.get("RUN_MAIN") == "true"

    def no_log(*a, **kw):
        return None

    for frame in inspect.stack():
        if "self" in frame.frame.f_locals:
            if isinstance(frame.frame.f_locals["self"], ServerHandler):
                server_handler = frame.frame.f_locals["self"]
                if hasattr(server_handler, "request_handler"):
                    server_handler.request_handler.log_message = no_log
    yield


def get_project_root() -> Path:
    """Returns the absolute path of the project."""
    # Daniel: I'm not sure if this is correct, it just works on a simple
    # Django project.
    kolo_dir = create_kolo_directory()
    project_folder = kolo_dir.parent
    return project_folder


@hide_from_runserver()
def kolo_web_router(request: HttpRequest) -> HttpResponse:
    request.get_host()  # Trigger any ALLOWED_HOSTS error
    path = request.path
    if path == "/_kolo/" or path == "/_kolo" or path.startswith("/_kolo/traces/"):
        return kolo_web_home(request)
    elif path.startswith("/_kolo/static/"):
        static_dir = os.path.join(os.path.dirname(__file__), "web", "static")
        file_path = os.path.join(static_dir, request.path[len("/_kolo/static/") :])

        if os.path.exists(file_path):
            mime_type, encoding = mimetypes.guess_type(file_path)
            return FileResponse(  # type: ignore # seems iffy and difficult to fix with little benefit
                open(file_path, "rb"),
                content_type=mime_type or "application/octet-stream",
            )
        else:
            return HttpResponseNotFound("File not found")
    elif path.startswith("/_kolo/api/generate-test/"):
        return kolo_web_api_generate_test(request)
    elif path.startswith("/_kolo/api/print-test/"):
        return kolo_web_api_print_test(request)
    elif path.startswith("/_kolo/api/traces/"):
        if request.method == "GET":
            return kolo_web_api_get_trace(request)
        elif request.method == "DELETE":
            return kolo_web_api_delete_trace(request)
        else:
            return HttpResponseNotFound("Kolo Web: Not Found")
    elif path.startswith("/_kolo/api/latest-traces/"):
        return kolo_web_api_latest_traces(request)
    elif path.startswith("/_kolo/api/save-test/"):
        return kolo_web_api_save_test(request)
    elif path.startswith("/_kolo/api/config/"):
        return kolo_web_api_config(request)
    elif path.startswith("/_kolo/api/source-file/"):
        return kolo_web_api_source_file(request)
    else:
        return HttpResponseNotFound("Kolo Web: Not Found")


def kolo_web_api_generate_test(request: HttpRequest) -> HttpResponse:
    trace_id = request.path.replace("/_kolo/api/generate-test/", "").replace("/", "")

    from .generate_tests import build_test_context, create_test_plan

    test_class = "MyTestCase"
    test_name = "test_my_view"

    config = load_config()
    context = build_test_context(
        trace_id, test_class=test_class, test_name=test_name, config=config
    )
    plan = create_test_plan(config, context)

    return JsonResponse({"test_code": plan.render(), "plan": plan.as_json()})


def kolo_web_api_print_test(request: HttpRequest) -> HttpResponse:
    # Intended solely for for djangocon booth demo
    trace_id = request.path.replace("/_kolo/api/print-test/", "").replace("/", "")

    from .generate_tests import generate_from_trace_ids

    test_class = "MyTestCase"
    test_name = "test_my_view"

    test_code = generate_from_trace_ids(
        trace_id, test_class=test_class, test_name=test_name
    )

    # These are intentionally not in our dependencies
    # We don't want our users to have to install escpos and pillow
    from escpos.printer import Usb
    from PIL import Image

    printer = Usb(0x04B8, 0x0E20, 0, profile="TM-T88III")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "mark-and-text-black.png")
    img = Image.open(image_path)

    max_width = 512
    current_width, current_height = img.size
    scale_ratio = max_width / float(current_width)
    new_height = int(scale_ratio * current_height)
    img = img.resize((max_width, new_height))

    printer.image(img, center=True)
    printer.text("\n\n\n")

    printer.set(align="left")

    printer.text(test_code)
    printer.text("\n\n\n")
    printer.text("*" * 48)
    printer.text("\nNOW YOU HAVE THE RECEIPT")
    printer.text("\nSEE MORE AT KOLO.APP/TESTGEN")
    printer.cut()

    stdout = ""
    stderr = ""
    # Now actually run the test as well
    import subprocess

    output = subprocess.run(
        ["kolo", "generate-test", "--unittest", "--use-plan", "--and-run", trace_id],
        capture_output=True,
        text=True,
    )
    stdout = output.stdout
    stderr = output.stderr

    printer.text(stderr)
    printer.cut()

    return JsonResponse({"ok": True, "stdout": stdout, "stderr": stderr})


@conditional_page
def kolo_web_api_get_trace(request: HttpRequest) -> HttpResponse:
    trace_id = request.path.replace("/_kolo/api/traces/", "").replace("/", "")

    from .db import load_trace_from_db

    db_path = setup_db()

    msgpack_data, created_at = load_trace_from_db(db_path, trace_id)
    response = HttpResponse(msgpack_data, content_type="application/msgpack")
    # When Chrome (Blink) and Safari (WebKit) do a `fetch()` request, they include the `If-None-Match` and
    # `If-Modified-Since` headers which allow for `ETag` (or `Last-Modified`) matching and returning a
    # 304 (Not Modified) response. FireFox (Gecko) only does so if a {cache: "force-cache"} value is given as options.
    last_modified = parse_datetime(created_at)
    if last_modified is not None:
        response["Last-Modified"] = http_date(last_modified.timestamp())
    response["ETag"] = trace_id
    # Once we've seen the trace, don't even try asking for the URL again for a while (a month) - because the traces are
    # ostensibly immutable, we should only really expect to *need* to ask for them again upon cache eviction
    patch_response_headers(response, cache_timeout=86400 * 28)
    return response


def kolo_web_api_delete_trace(request: HttpRequest) -> HttpResponse:
    trace_id = request.path.replace("/_kolo/api/traces/", "").replace("/", "")

    from .db import delete_traces_by_id

    db_path = setup_db()

    count = delete_traces_by_id(db_path, (trace_id,))

    return JsonResponse({"deleted": count})


def kolo_web_api_save_test(request: HttpRequest) -> HttpResponse:
    # Find out the absolute path of the project
    project_folder = get_project_root()

    data = json.loads(request.body.decode("utf-8"))
    file_content: str = data["content"]
    relative_file_path: List[str] = data["path"]
    file_path = project_folder / os.path.join(*relative_file_path)

    # Create the file directory if it does not exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as file:
        file.write(file_content)

    return JsonResponse({"file_path": f"{file_path}"})


def kolo_web_api_config(request: HttpRequest) -> HttpResponse:
    return JsonResponse(load_config())


def kolo_web_api_latest_traces_etag(request, *a, **kwargs):
    # This decorator runs first as a pre-condition (before the `Last-Modified` version) so bind to request to
    # avoid doing more stat syscalls for the etag.
    request._db_last_modified = get_db_last_modified()
    if request._db_last_modified is not None:
        return sha1(request._db_last_modified.isoformat().encode("utf-8")).hexdigest()
    return None


def kolo_web_api_latest_traces_last_modified(request, *a, **kwargs):
    return getattr(request, "_db_last_modified", None)


def kolo_web_api_source_file(request: HttpRequest) -> HttpResponse:
    file_path = request.GET["path"]

    file_path_parts = file_path.split("/")
    filename = file_path_parts.pop()
    assert filename.endswith(".py")

    project_path = get_project_root()
    absolute_file_path = os.path.join(project_path, *file_path_parts, filename)

    with open(absolute_file_path, "r") as f:
        content = f.read()

    return JsonResponse(
        {
            "path": absolute_file_path,
            "content": content,
        }
    )


@cache_control(max_age=1)
@condition(
    etag_func=kolo_web_api_latest_traces_etag,
    last_modified_func=kolo_web_api_latest_traces_last_modified,
)
def kolo_web_api_latest_traces(request: HttpRequest) -> HttpResponse:
    from .db import db_connection

    db_path = setup_db()
    with db_connection(db_path) as connection:
        needs_reversed_order = False
        reached_top = False

        if "anchor" in request.GET and "showNext" in request.GET:
            # this is a pagination request

            anchor = request.GET["anchor"]
            show_next = int(request.GET["showNext"])

            limit = abs(show_next)

            # Positive show_next value means we're going back in time (loading _more_ traces),
            # negative value is for going forward in time (loading traces the user has previously seen before going back).

            if show_next > 0:
                # going back in time, trying to access older traces than the anchor

                query = "SELECT id FROM traces WHERE id < ? ORDER BY id desc LIMIT ?"
                cursor = connection.execute(query, (anchor, limit))
                rows = cursor.fetchall()
            else:
                # going forward in time, trying to access newer traces than the anchor

                query = "SELECT id FROM traces WHERE id > ? ORDER BY id LIMIT ?"
                needs_reversed_order = True
                # In order to get 10 newer traces, they need to be sorted in ascending order.
                # They have to be reversed later because the endpoint should always return traces from newest to oldest.

                cursor = connection.execute(query, (anchor, limit))
                rows = cursor.fetchall()

                if len(rows) < abs(limit):
                    # If there are less than 10 newer traces, we need to fetch some older traces to fill up the response.
                    cursor = connection.execute(
                        "SELECT id FROM traces ORDER BY id desc LIMIT ?", (abs(limit),)
                    )
                    rows = cursor.fetchall()

                    reached_top = True
                    needs_reversed_order = False
        else:
            # not a pagination request, we just want N latest traces

            limit = int(request.GET.get("showNext", 10))
            cursor = connection.execute(
                "SELECT id FROM traces ORDER BY id desc LIMIT ?", (limit,)
            )

            rows = cursor.fetchall()
            reached_top = True

    traces = list(chain.from_iterable(rows))

    if needs_reversed_order:
        traces = traces[::-1]
    try:
        last_modified = (
            request._db_last_modified.timestamp()  # type:ignore[attr-defined]
        )
    except AttributeError:
        last_modified = None
    response = JsonResponse(
        {
            "traces": traces,
            "isTop": reached_top,
            "lastModified": last_modified,
        }
    )
    return response
