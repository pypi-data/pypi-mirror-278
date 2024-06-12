from typing import List, Literal, TypeVar

from pydantic import BaseModel, Field

from seqthetic.dependencies import DependencySpec
from seqthetic.mapping import MappingSpec
from seqthetic.range import Range

T = TypeVar("T")
RawOrList = T | List[T]


class Vary(BaseModel):
    index: int = Field(..., ge=0)
    dependency: dict[str, list[float | str | Range]]
    mapping: dict[str, int] | None = None  # todo
    op_type: Literal["vary"] = Field(default="vary")
    combine_type: Literal["zip", "product"] = Field(default="product")


class Insert(BaseModel):
    index: int
    ratio_original: list[float]
    ratio_inserted: float
    dependency: DependencySpec
    mapping: MappingSpec = Field(default_factory=MappingSpec)
    op_type: Literal["insert"] = Field(default="insert")


class Identity(BaseModel):
    op_type: Literal["identity"] = Field(default="identity")


class Remove(BaseModel):
    index: int | list[int]
    ratio_new: list[float]
    op_type: Literal["remove"] = Field(default="remove")


class Shuffle(BaseModel):
    op_type: Literal["shuffle"] = Field(default="shuffle")
    times: int = Field(default=1, ge=1)


DomainOp = Vary | Insert | Remove | Shuffle
