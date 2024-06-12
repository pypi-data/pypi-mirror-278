import datetime
import json
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field, computed_field, field_validator

from seqthetic.dependencies import adapter
from seqthetic.dependencies.base import BaseDependency
from seqthetic.mapping import MappingSpec
from seqthetic.seed import Seed, SpecSeed

from .dependencies import DependencySpec
from .utils import ID, SizeValue
from .vocabulary import VocabularySpec

# todo: insights into tasks;


class DomainSpec(BaseModel):
    """a kind of data with designated dependency"""

    id: str = ID
    mixture_ratio: float = Field(..., gt=0, le=1)  # ratio of token in the total dataset
    num_sequence: int = 0  # number of sequences in this domain
    num_token: int = 0  # number of total tokens in this domain
    mapping: MappingSpec = Field(default_factory=MappingSpec)
    dependency: DependencySpec
    comment: str = ""

    def set_dependency_seeds(self, seed: Seed):
        self.dependency.seed = seed


class SplitSpec(BaseModel):
    """
    Two advised usages:
    1. shuffle the dataset: most random and homogenous. just set shuffle_dataset to True, it takes precedence over other shuffle settings
    2. preserve domain order, shuffle sequence order in domains: default mode, useful for curriculum learning
    set shuffle_dataset to False, shuffle_domain_order to False, shuffle_domain_sequence to True
    3. shuffle domain order and sequence order: relatively homogenous shuffle_domain_order to True

    """

    # whether to shuffle across all dataset
    shuffle_dataset: bool = False
    shuffle_domain_order: bool = False
    # whether to shuffle the order of the sequences in each domains
    shuffle_domain_sequence: bool = True
    # ratio between train, val, test, counted by number of sequences
    split_ratio: List[float] = Field(default_factory=lambda: [0.8, 0.1, 0.1])

    def get_index(self, num_items: int):
        train_index = int(self.split_ratio[0] * num_items)
        val_index = train_index + int(self.split_ratio[1] * num_items)
        return train_index, val_index

    @field_validator("split_ratio")
    def check_split_ratio(cls, split_ratio):
        if abs(sum(split_ratio) - 1) > 1e-6:
            raise ValueError("sum of split_ratio should be 1")
        return split_ratio


class SynthesisSpec(BaseModel):
    id: str = ID
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    name: str = ""
    """total token specified by user, real number may vary depending on the randomness in domains"""
    num_token: SizeValue
    split: SplitSpec = Field(default_factory=SplitSpec)
    vocabulary: VocabularySpec
    domains: List[DomainSpec]
    seeds: SpecSeed = Field(default_factory=SpecSeed)

    def model_post_init(self, __context):
        self.init_seeds()
        self.check_mixture_sum()
        self.update_domain_stat()

    @computed_field
    @property
    def num_token_exact(self) -> int:
        return sum([domain.num_token for domain in self.domains])

    @staticmethod
    def register_dependency(dependency: BaseDependency):
        adapter.register(dependency)

    def init_seeds(self, set_domain_seed=True, set_vocab_seed=True):
        # requires creating new seed
        if len(self.seeds.vocabulary.seeds) == 0:
            seeds = SpecSeed(
                vocabulary=Seed(seed_schema=self.vocabulary.seed_schema),
                domains=[
                    Seed(seed_schema=domain.dependency.seed_schema)
                    for domain in self.domains
                ],
                split=Seed(
                    seed_schema=[
                        "shuffle_dataset",
                        "shuffle_domain_order",
                        "shuffle_domain_sequence",
                    ]
                ),
            )

            self.seeds = seeds
        # if not empty, means contains seeds, often for deserializing
        # move seed to vocabulary and depdendency

        self.vocabulary.set_seed(self.seeds.vocabulary)
        if set_domain_seed:
            for domain, seed in zip(self.domains, self.seeds.domains):
                domain.set_dependency_seeds(seed)

        return self

    def seed_from_domains(self):
        self.seeds.domains = [domain.dependency.seed for domain in self.domains]

    def check_mixture_sum(self):
        mixtures = sum([domain.mixture_ratio for domain in self.domains])
        if abs(mixtures - 1) > 1e-6:
            raise ValueError("sum of mixture ratio should be 1")
        return self

    def update_domain_stat(self):
        for domain in self.domains:
            domain.num_token = round(self.num_token * domain.mixture_ratio)
            seq_len = domain.dependency.sequence_length
            if seq_len.constant:
                domain.num_sequence = int(
                    domain.num_token // domain.dependency.sequence_length.min
                )
            # todo: for not constant length sequence
        return self

    def save(self, path: str = "./"):
        """save the dataset spec to a json file"""
        spec_json = self.model_dump_json(indent=4)
        name = self.name or self.id
        path = Path(path) / f"{name}.synspec.json"
        print(f"Save the spec file to {path}")
        with open(path, "w") as f:
            f.write(spec_json)
        return str(path)

    @classmethod
    def load(cls, path: str = ""):
        with open(path, "r") as f:
            spec_dict = json.load(f)
            spec = SynthesisSpec.model_validate(spec_dict)

        return spec
