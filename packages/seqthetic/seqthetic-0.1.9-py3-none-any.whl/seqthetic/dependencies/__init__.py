from typing import Union, Annotated

from seqthetic.dependencies.fbm import FBMDependency
from seqthetic.dependencies.function import FunctionDependency
from seqthetic.dependencies.random import RandomDependency
from seqthetic.dependencies.adapter import DependencyAdapter
from pydantic import PlainValidator

adapter = DependencyAdapter((FBMDependency, RandomDependency, FunctionDependency))
DependencySpec = Annotated[
    Union[FBMDependency, RandomDependency, FunctionDependency],
    adapter.make_serializer(),
    adapter.make_validator(),
]
