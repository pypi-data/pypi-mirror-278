from typing import Literal
from pydantic import BaseModel, Field

from seqthetic.range import Range
from seqthetic.vary.compose_ops import ComposeOp, Product, Zip
from seqthetic.vary.domain_ops import (
    Identity,
    Insert,
    Remove,
    Shuffle,
    Vary,
)
from devtools import debug
from seqthetic.synthesis_spec import DomainSpec, SynthesisSpec
from itertools import product
import random


class AtomShuffle(BaseModel):
    ids: tuple[str]
    op_type: Literal["atom_shuffle"] = Field(default="atom_shuffle")


class AtomicMappingVary(BaseModel):
    index: int = Field(..., ge=0)
    value: dict[str, int]  # todo
    op_type: Literal["atom_mapping_vary"] = Field(default="atom_mapping_vary")


class AtomicDependencyVary(BaseModel):
    index: int = Field(..., ge=0)
    value: dict[str, float | str | Range]
    op_type: Literal["atom_dependency_vary"] = Field(default="atom_dependency_vary")


AtomicVary = AtomicDependencyVary | AtomicMappingVary
AtomicDomainOp = AtomicVary | Insert | Remove | AtomShuffle | Identity
DomainTransform = list[AtomicDomainOp]


def op_to_transform(spec: SynthesisSpec, compose_op: ComposeOp):

    def expand_to_transform_helper(
        spec: SynthesisSpec, compose_op: ComposeOp, merged=False
    ):
        if isinstance(compose_op, Shuffle):
            return to_atomic_shuffle(spec, compose_op, merged=merged)

        elif isinstance(compose_op, Vary):
            return to_atomic_vary(compose_op, merged=merged)
        elif isinstance(compose_op, Insert) or isinstance(compose_op, Remove):
            return [[compose_op]] if not merged else [compose_op]
        elif isinstance(compose_op, Product):
            factors = []
            for op in compose_op.ops:
                factors.append(expand_to_transform_helper(spec, op, merged=True))

            return list(product(*factors))

            # todo: merge

        elif isinstance(compose_op, Zip):
            factors = []
            for op in compose_op.ops:
                factors.append(expand_to_transform_helper(spec, op, merged=True))
            res = [[el for el in e] for e in zip(*factors)]

            return res

    transforms = expand_to_transform_helper(spec, compose_op)
    transforms = [[t for t in transform] for transform in transforms]
    return transforms


def transform_domain(spec: SynthesisSpec, transform: DomainTransform) -> SynthesisSpec:
    debug("vary spec domain")
    new_spec = spec.model_copy(deep=True)
    for op in transform:
        if isinstance(op, AtomShuffle):
            domain_dict = {d.id: d for d in new_spec.domains}
            new_spec.domains = [domain_dict[id] for id in op.ids]
            continue

        if isinstance(op, AtomicDependencyVary):
            index = op.index
            new_dependency = new_spec.domains[index].dependency.model_copy(
                deep=True, update=op.value
            )

            new_dependency.init_seed()
            new_domain = DomainSpec(
                mixture_ratio=new_spec.domains[index].mixture_ratio,
                dependency=new_dependency,
            )
            new_spec.domains[index] = new_domain

        if isinstance(op, Insert):
            index = op.index
            new_domain = DomainSpec(
                mixture_ratio=op.ratio_inserted,
                mapping=op.mapping,
                dependency=op.dependency,
            )
            new_spec.domains.insert(index, new_domain)
        if isinstance(op, Remove):
            if isinstance(index, list):
                for i in index:
                    del new_spec.domains[i]
            else:
                del new_spec.domains[index]
    new_spec.update_domain_stat()
    new_spec.seed_from_domains()
    return new_spec


def to_atomic_shuffle(spec: SynthesisSpec, domain_op: Shuffle, merged=False):
    domain_ids = set()
    for _ in range(domain_op.times):
        domains = [d for d in spec.domains]
        random.shuffle(domains)
        ids = (d.id for d in domains)
        max_tries = 5
        tries = 0
        while ids in domain_ids and tries < max_tries:
            random.shuffle(domains)
            ids = (d.id for d in domains)
            tries += 1
        domain_ids.add(ids)
    result = (
        [[AtomShuffle(ids=ids)] for ids in domain_ids]
        if not merged
        else [AtomShuffle(ids=ids) for ids in domain_ids]
    )
    return result


def to_atomic_vary(domain_op: Vary, merged=False):
    dep_values = list(domain_op.dependency.values())
    if domain_op.combine_type == "product":
        new_values = list(product(*dep_values))
    else:
        value_lengths = set(len(value) for value in dep_values)
        if len(value_lengths) != 1:
            raise ValueError("do not match as required by zip mode")
        new_values = list(zip(*dep_values))
    keys = [list(domain_op.dependency.keys())] * len(new_values)
    result = []
    for key, value in zip(keys, new_values):
        pairs = [
            (k, v) if isinstance(v, Range) else (k, Range(min=v, max=v))
            for k, v in zip(key, value)
        ]
        atomic_vary = AtomicDependencyVary(index=domain_op.index, value=dict(pairs))
        (result.append([atomic_vary]) if not merged else result.append(atomic_vary))

    return result
