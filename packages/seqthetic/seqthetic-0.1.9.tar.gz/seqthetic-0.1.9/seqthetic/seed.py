from typing import List

import numpy as np
from pydantic import BaseModel, Field, model_validator


def make_seed():
    return np.random.SeedSequence().entropy


class Seed(BaseModel):
    seed_schema: List[str] = Field(default_factory=list)
    seeds: dict[str, int] = Field(default_factory=dict)
    
    def model_post_init(self, __context):
        self.init_seeds()

    def init_seeds(self):
        if len(self.seeds) != 0:
            # for deserializing
            return self
        self.seeds = {field: make_seed() for field in self.seed_schema}
        return self

    def __getitem__(self, item):
        return self.seeds[item]
    
    def get_rng(self, field: str, count=1, return_list=False):
        seed = self.seeds[field]
        if count > 1:
            ss = np.random.SeedSequence(seed)
            return [np.random.default_rng(s) for s in ss.spawn(count)]
        elif return_list:
            return [np.random.default_rng(seed)]
        else:
            return np.random.default_rng(seed)


class SpecSeed(BaseModel):
    vocabulary: Seed = Field(default_factory=Seed)
    domains: List[Seed]  = Field(default_factory=list)
    split: Seed = Field(default_factory=Seed)
