from __future__ import annotations

import platform
from datetime import datetime, timezone

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader

from ..config import load_config
from ..db import load_trace_from_db, setup_db
from ..serialize import load_msgpack
from ..utils import maybe_format
from ..version import __version__
from .format import format_intermediate
from .plan import Plan, build_steps, load_hooks, run_plan_hooks
from .processors import load_processors, run_processors


class KoloPackageLoader(PackageLoader):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Work around UNC path mishandling:
        # https://github.com/pallets/jinja/issues/1675
        if platform.system() == "Windows":
            unc_prefix = "\\\\?\\"
            if self._template_root.startswith(unc_prefix):  # pragma: no cover
                self._template_root = self._template_root[len(unc_prefix) :]


env = Environment(
    loader=ChoiceLoader(
        (
            FileSystemLoader(""),
            KoloPackageLoader("kolo"),
        )
    )
)


def load_traces(db_path, trace_ids):
    traces = {}
    for trace_id in trace_ids:
        msgpack_data, _ = load_trace_from_db(db_path, trace_id)
        trace = load_msgpack(msgpack_data)
        traces[trace_id] = {
            "frames": trace["frames_of_interest"],
            "trace": trace,
        }
    return traces


def build_test_context(
    *trace_ids: str,
    test_class: str,
    test_name: str,
    config,
    include_generation_timestamp=True,
    use_saved_schemas=False,
):
    processors = load_processors(config)

    db_path = setup_db()
    traces = load_traces(db_path, trace_ids)

    context = {
        "_config": config,
        "_db_path": db_path,
        "_traces": traces,
        "_use_saved_schemas": use_saved_schemas,
        "base_test_case": "TestCase",
        "kolo_version": __version__,
        "now": datetime.now(timezone.utc) if include_generation_timestamp else None,
        "test_class": test_class,
        "test_name": test_name,
    }
    run_processors(processors, context)
    return context


def create_test_plan(config, context, pytest=True) -> Plan:
    plan = Plan(build_steps(context, pytest=pytest), pytest, context)
    plan_hooks = load_hooks(config)
    return run_plan_hooks(plan, plan_hooks)


def generate_from_trace_ids(
    *trace_ids: str,
    test_class: str,
    test_name: str,
    template_name: str = "",
    config=None,
    include_generation_timestamp=True,
    use_saved_schemas=False,
    pytest=True,
    use_plan=False,
) -> str:
    if config is None:
        config = load_config()
    context = build_test_context(
        *trace_ids,
        test_class=test_class,
        test_name=test_name,
        config=config,
        include_generation_timestamp=include_generation_timestamp,
        use_saved_schemas=use_saved_schemas,
    )
    if use_plan:
        plan = create_test_plan(config, context, pytest)
        rendered = plan.render()
    else:
        if not template_name:
            if pytest:
                template_name = "django_request_pytest.py.j2"
            else:
                template_name = "django_request_test.py.j2"
        template = env.get_template(template_name)
        rendered = template.render(**context)
    return maybe_format(rendered)


def generate_test_intermediate_format(
    *trace_ids: str,
    test_class: str,
    test_name: str,
    config=None,
    include_generation_timestamp=True,
    use_saved_schemas: bool = False,
):
    if config is None:  # pragma: no branch
        config = load_config()
    processors = load_processors(config)

    db_path = setup_db()
    traces = load_traces(db_path, trace_ids)

    context = {
        "_config": config,
        "_db_path": db_path,
        "_traces": traces,
        "_use_saved_schemas": use_saved_schemas,
        "base_test_case": "TestCase",
        "kolo_version": __version__,
        "now": datetime.now(timezone.utc) if include_generation_timestamp else None,
        "test_class": test_class,
        "test_name": test_name,
    }

    for processor in processors:  # pragma: no branch
        output = processor(context)
        if output:
            context.update(output)
        if "sections" in context and "sql_fixtures" in context["sections"][0]:
            yield from format_intermediate(context)
            break
