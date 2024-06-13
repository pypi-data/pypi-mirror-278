from typing import List

import numpy as np
from pydantic import Field

from seqthetic.dependencies.base import BaseDependency, DependencyResult, SchemaList
from seqthetic.range import FlexibleRange
from seqthetic.utils import make_digitizer


class FunctionDependency(BaseDependency):
    """Dependency from a function"""

    generator: str = "function"

    function: str

    # python code for the function, for example "func = lambda x: np.sin(x)", please use numpy function recommended
    # please name the function as "func"
    discretize_ratio: FlexibleRange = Field(..., gt=0, le=1)  # ratio for binning
    metadata_schema: List[str] = SchemaList(["sequence_length", "discretize_ratio"])
    custom_seed_schema: List[str] = SchemaList(["discretize_ratio"])

    def make_function_dependency(self, num_sequence: int):
        length_rng = self.seed.get_rng("sequence_length")
        binning_ratio_rng = self.seed.get_rng("discretize_ratio")
        lengths = length_rng.integers(
            self.sequence_length.min, self.sequence_length.max, num_sequence
        )
        env = {}
        exec(self.function, {"np": np}, env)
        func = env["func"]
        binning_ratios = binning_ratio_rng.uniform(
            self.discretize_ratio.min, self.discretize_ratio.max, num_sequence
        )

        dependencies_raw = [func(np.arange(length)) for length in lengths]

        # make digitizer
        digitizers = [make_digitizer(ratio) for ratio in binning_ratios]
        dependencies = [
            list(digitize(dr)) for dr, digitize in (dependencies_raw, digitizers)
        ]
        metadata = [
            {"sequence_length": l, "binning_ratio": b}
            for l, b in zip(lengths, binning_ratios)
        ]
        return DependencyResult(dependencies, metadata)
