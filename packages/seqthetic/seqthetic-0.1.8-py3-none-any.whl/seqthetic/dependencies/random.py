from typing import List

from seqthetic.dependencies.base import (BaseDependency, DependencyResult,
                                         SchemaList)
from seqthetic.range import FlexibleRange


class RandomDependency(BaseDependency):
    """Dependency from random number generator"""

    generator: str = "random"
    num_dependency: FlexibleRange
    metadata_schema: List[str] = SchemaList(["num_dependency"])
    custom_seed_schema: List[str] = SchemaList(["num_dependency"])

    def make_dependency(self, num_sequence: int):
        dep_rng = self.seed.get_rng("num_dependency")
        length_rng = self.seed.get_rng("sequence_length")
        num_dependencies = dep_rng.integers(
            self.num_dependency.min, self.num_dependency.max, num_sequence
        ) if not self.num_dependency.constant else [int(self.num_dependency.min)] * num_sequence
        sequence_lengths = length_rng.integers(
            self.sequence_length.min, self.sequence_length.max, num_sequence
        ) if not self.sequence_length.constant else [int(self.sequence_length.min)] * num_sequence
        dependencies = [
            dep_rng.integers(num_dependency, size=length)
            for num_dependency, length in zip(num_dependencies, sequence_lengths)
        ]
        metadata = [
            {"num_dependency": n, "sequence_length": l}
            for n, l in zip(num_dependencies, sequence_lengths)
        ]
        return DependencyResult(dependencies, metadata)