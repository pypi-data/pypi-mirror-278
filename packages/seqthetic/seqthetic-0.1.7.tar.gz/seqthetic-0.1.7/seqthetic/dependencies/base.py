from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

import numpy as np
from pydantic import BaseModel, Field, model_validator

from seqthetic.range import FlexibleRange
from seqthetic.seed import Seed


@dataclass
class DependencyResult:
    dependencies: List[np.ndarray]
    metadata: List[dict]


class BaseDependency(BaseModel, ABC):
    generator: str = ""
    # fields in metadata field in dataset
    metadata_schema: List[str] = Field(
        default_factory=lambda: ["sequence_length"], exclude=True
    )
    base_seed_schema: List[str] = Field(
        default_factory=lambda: ["sequence_length"], exclude=True
    )
    custom_seed_schema: List[str] = Field(default_factory=list, exclude=True)
    sequence_length: FlexibleRange
    seed: Seed = Field(default_factory=Seed, exclude=True)

    @property
    def seed_schema(self) -> list[str]:
        return self.base_seed_schema + self.custom_seed_schema

    def init_seed(self):
        self.seed = Seed(seed_schema=self.seed_schema)

    @model_validator(mode="after")
    def must_rewrite_generator(self):
        if not self.generator:
            raise ValueError("Please fill generator with proper value")
        return self

    @model_validator(mode="after")
    def validate_metadata_fields(self):
        model_fields = self.model_dump().keys()
        for field in self.metadata_schema:
            if field not in model_fields:
                raise ValueError(f"{field} in metadata schema not in the model fields")

        return self

    @abstractmethod
    def make_dependency(self, num_sequence: int) -> DependencyResult:
        pass


def SchemaList(fields: list[str]):
    return Field(default_factory=lambda: fields.copy(), exclude=True)
