from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Protocol, Tuple


class Step(Protocol):
    indent_delta: ClassVar[int]

    def render(self, pytest): ...


@dataclass(frozen=True)
class CodeComment:
    comment: str
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        return f"# {self.comment}\n"


@dataclass(frozen=True)
class EmptyLine:
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        return "\n"


@dataclass(frozen=True)
class Import:
    import_path: str
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        return f"{self.import_path}\n"


@dataclass(frozen=True)
class TestClass:
    name: str
    parents: str
    indent_delta: ClassVar[int] = 1

    def render(self, pytest):
        return f"class {self.name}({self.parents}):\n"


@dataclass(frozen=True)
class EndClass:
    indent_delta: ClassVar[int] = -1

    def render(self, pytest):
        return ""


@dataclass(frozen=True)
class Code:
    code: str
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        return f"{self.code}\n"


@dataclass(frozen=True)
class Method:
    name: str
    indent_delta: ClassVar[int] = 1

    def render(self, pytest):
        return f"def {self.name}(self):\n"


@dataclass(frozen=True)
class EndMethod:
    indent_delta: ClassVar[int] = -1

    def render(self, pytest):
        return ""


@dataclass(frozen=True)
class TestFunction:
    name: str
    fixtures: Tuple[str]
    indent_delta: ClassVar[int] = 1

    def render(self, pytest):
        fixtures = ", ".join(self.fixtures)
        return f"def {self.name}({fixtures}):\n"


@dataclass(frozen=True)
class EndFunction:
    indent_delta: ClassVar[int] = -1

    def render(self, pytest):
        return ""


@dataclass(frozen=True)
class With:
    call: str
    args: str
    indent_delta: ClassVar[int] = 1

    def render(self, pytest):
        return f"with {self.call}({self.args}):\n"


@dataclass(frozen=True)
class EndWith:
    indent_delta: ClassVar[int] = -1

    def render(self, pytest):
        return ""


@dataclass(frozen=True)
class AssertEqual:
    left: str
    right: str
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        if pytest:
            return f"assert {self.left} == {self.right}\n"
        return f"self.assertEqual({self.left}, {self.right})\n"


@dataclass(frozen=True)
class AssertStatusCode:
    status_code: int
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        if pytest:
            return f"assert response.status_code == {self.status_code}\n"
        return f"self.assertEqual(response.status_code, {self.status_code})\n"


@dataclass(frozen=True)
class AssertResponseJson:
    response_json: str
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        if pytest:
            return f"assert response.json() == {self.response_json}\n"
        return f"self.assertEqual(response.json(), {self.response_json})\n"


@dataclass(frozen=True)
class AssertTemplateUsed:
    template_name: str
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        if pytest:
            assertTemplateUsed = "assertTemplateUsed"
        else:
            assertTemplateUsed = "self.assertTemplateUsed"
        return f"{assertTemplateUsed}(response, {repr(self.template_name)})\n"


@dataclass(frozen=True)
class RegisterMocket:
    method: str
    url: str
    status_code: int
    body: Optional[str]
    json_body: Optional[str]
    content_type: str
    indent_delta: ClassVar[int] = 0

    @classmethod
    def from_outbound_request(cls, outbound_request):
        request = outbound_request["request"]
        response = outbound_request["response"]
        return cls(
            request["method"],
            request["url"],
            response["status_code"],
            response["body"],
            response.get("json_body", None),
            response["content_type"],
        )

    def render(self, pytest):
        rendered = f"""\
Entry.single_register(
    Entry.{self.method},
    "{self.url}",
    status={self.status_code},
"""
        if self.json_body:
            rendered += f"    body=json.dumps({self.json_body}),\n"
        elif self.body:
            rendered += f"    body={repr(self.body)},\n"
        if self.content_type:
            rendered += f'    headers={{"Content-Type": {repr(self.content_type)}}},'
        rendered += ")\n"
        return rendered


@dataclass(frozen=True)
class DjangoTestClient:
    method: str
    path_info: str
    query_params: str
    request_body: str
    headers: Dict[str, Any]
    indent_delta: ClassVar[int] = 0

    def render(self, pytest):
        if pytest:
            client = "client"
        else:
            client = "self.client"
        rendered = f"""\
response = {client}.{self.method}(
    {repr(self.path_info)},
    {self.query_params}{self.request_body},
"""
        for header, value in self.headers.items():
            rendered += f"    {header}={repr(value)},\n"
        rendered += ")\n"
        return rendered


@dataclass(frozen=True)
class DjangoField:
    name: str
    value: str


@dataclass(frozen=True)
class CreateModel:
    module: str
    model: str
    fields: List[DjangoField]
    defaults: List[DjangoField]
    defines_variable_name: str
    method: str = "get_or_create"
    indent_delta: ClassVar[int] = 0

    @property
    def import_path(self):
        return f"from {self.module} import {self.model}"

    @property
    def model_path(self):
        return f"{self.module}.{self.model}"

    @classmethod
    def from_fixture(cls, fixture):
        return cls(
            module=fixture.module,
            model=fixture.model,
            fields=[DjangoField(f.name, f.value_repr) for f in fixture.fields],
            defaults=[
                DjangoField(fixture.primary_key.name, fixture.primary_key.value_repr)
            ],
            defines_variable_name=fixture.variable_name,
        )

    def render(self, pytest):
        rendered = f"{self.defines_variable_name}"
        if self.method == "get_or_create":
            rendered += ", _created"

        rendered += f" = {self.model}.objects.{self.method}(\n"
        for field in self.fields:
            rendered += f"    {field.name}={field.value},\n"

        rendered += "    defaults={\n"
        for field in self.defaults:
            rendered += f"        {repr(field.name)}: {field.value},\n"
        rendered += "    },\n"
        rendered += ")\n"
        return rendered


@dataclass(frozen=True)
class UpdateModel:
    model: str
    fields: List[DjangoField]
    references_variable_name: str
    indent_delta: ClassVar[int] = 0

    @classmethod
    def from_fixture(cls, fixture):
        return cls(
            model=fixture.model,
            fields=[DjangoField(f.name, f.value_repr) for f in fixture.fields],
            references_variable_name=fixture.variable_name,
        )

    def render(self, pytest):
        for field in self.fields:
            rendered = f"{self.references_variable_name}.{field.name} = {field.value}\n"

        rendered += f"{self.references_variable_name}.save()\n"
        return rendered


@dataclass(frozen=True)
class FactoryCreate:
    module: str
    factory: str
    fields: List[DjangoField]
    defines_variable_name: str
    indent_delta: ClassVar[int] = 0

    @classmethod
    def from_fixture(cls, fixture):
        return cls(
            module=fixture.module,
            factory=fixture.factory,
            fields=[DjangoField(f.name, f.value_repr) for f in fixture.fields],
            defines_variable_name=fixture.variable_name,
        )

    def render(self, pytest):
        rendered = f"{self.defines_variable_name} = {self.factory}.create(\n"
        for field in self.fields:
            rendered += f"    {field.name}={field.value},\n"
        rendered += ")\n"
        return rendered


@dataclass(frozen=True)
class AssertInsert:
    module: str
    model: str
    lookup_fields: List[DjangoField]
    assert_fields: List[DjangoField]
    defines_variable_name: str
    indent_delta: ClassVar[int] = 0

    @property
    def import_path(self):
        return f"from {self.module} import {self.model}"

    @property
    def model_path(self):
        return f"{self.module}.{self.model}"

    @classmethod
    def from_fixture(cls, fixture):
        lookup_fields, assert_fields = fixture.get_fields()
        return cls(
            module=fixture.module,
            model=fixture.model,
            lookup_fields=[DjangoField(f.name, f.value_repr) for f in lookup_fields],
            assert_fields=[DjangoField(f.name, f.value_repr) for f in assert_fields],
            defines_variable_name=fixture.variable_name,
        )

    def render(self, pytest):
        rendered = f"{self.defines_variable_name} = {self.model}.objects.get(\n"
        for field in self.lookup_fields:
            rendered += f"    {field.name}={field.value},\n"
        rendered += ")\n"
        for field in self.assert_fields:
            if pytest:
                rendered += f"assert {self.defines_variable_name}.{field.name} == {field.value}\n"
            else:
                rendered += f"self.assertEqual({self.defines_variable_name}.{field.name}, {field.value})\n"

        return rendered


@dataclass(frozen=True)
class AssertUpdate:
    model: str
    fields: List[DjangoField]
    references_variable_name: str
    indent_delta: ClassVar[int] = 0

    @classmethod
    def from_fixture(cls, fixture):
        return cls(
            model=fixture.model,
            fields=[DjangoField(f.name, f.value_repr) for f in fixture.fields],
            references_variable_name=fixture.variable_name,
        )

    def render(self, pytest):
        rendered = f"{self.references_variable_name}.refresh_from_db()\n"
        for field in self.fields:
            if pytest:
                rendered += f"assert {self.references_variable_name}.{field.name} == {field.value}\n"
            else:
                rendered += f"self.assertEqual({self.references_variable_name}.{field.name}, {field.value})\n"
        return rendered


@dataclass(frozen=True)
class AssertDelete:
    model: str
    fields: List[DjangoField]
    indent_delta: ClassVar[int] = 0

    @classmethod
    def from_fixture(cls, fixture):
        return cls(
            model=fixture.model,
            fields=[DjangoField(f.name, f.value_repr) for f in fixture.fields],
        )

    def grouped_fields(self):
        fields: Dict[str, List[str]] = {}
        for field in self.fields:
            fields.setdefault(field.name, []).append(field.value)
        return fields

    def render(self, pytest):
        if pytest:
            rendered = "assert not "
        else:
            rendered = "self.assertFalse("
        rendered += f"{self.model}.objects.filter(\n"

        for name, values in self.grouped_fields().items():
            if len(values) == 1:
                value = values[0]
                rendered += f"    {name}={value},\n"
            else:
                joined_values = ", ".join(values)
                rendered += f"    {name}__in=({joined_values}),\n"
        if pytest:
            rendered += ").exists()\n"
        else:
            rendered += ").exists())\n"
        return rendered
