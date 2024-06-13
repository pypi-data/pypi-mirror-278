from typing import Union
from pydantic import TypeAdapter, PlainSerializer, PlainValidator
from seqthetic.dependencies.base import BaseDependency


class DependencyAdapter:
    adapter: TypeAdapter
    dependencies: tuple[BaseDependency]

    def __init__(self, dependencies: tuple[BaseDependency]):
        self.dependencies = dependencies
        self.adapter = TypeAdapter(Union[dependencies])

    def register(self, dependency: BaseDependency):
        self.dependencies = (*self.dependencies, dependency)
        self.adapter = TypeAdapter(Union[self.dependencies])

    def __call__(self, v: any):
        return self.adapter.validate_python(v)

    def make_validator(self):
        return PlainValidator(lambda v: self.adapter.validate_python(v))

    def make_serializer(self):
        return PlainSerializer(lambda v: self.adapter.dump_python(v))
