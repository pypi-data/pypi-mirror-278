from enum import Enum

from pydantic import BaseModel, Field, field_validator

from seqthetic.vary.compose_ops import ComposeOp
from seqthetic.vary.compute_ops import ComputeOp

Mixtures = list[list[float]]
TotalTokenInput = list[ComputeOp | int]
class SeedConfig(BaseModel):
    change_vocab_sample: bool = True
    change_vocab_noise: bool = True
    change_domain: bool = True
    same: bool = False
    
class Variation(BaseModel):
    total_token: TotalTokenInput | None = Field(default=None) 
    mixture: Mixtures | None = Field(default=None)
    domain: ComposeOp | None = Field(default=None)
    seed: SeedConfig = SeedConfig() 

    @field_validator("mixture", mode="after")
    def check_mixture_sum_to_one(cls, mixtures: Mixtures):
        for i, mixture in enumerate(mixtures):
            if abs(sum(mixture) - 1) > 1e-6:
                raise ValueError(f"sum of mixture {i}  should be 1")
        return mixtures