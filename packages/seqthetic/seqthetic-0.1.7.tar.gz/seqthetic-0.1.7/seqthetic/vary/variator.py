from itertools import product

from pydantic import BaseModel, Field

from seqthetic.synthesis_spec import DomainSpec, SynthesisSpec
from seqthetic.spec_variation import SpecVariation
from seqthetic.vary.compose_ops import ComposeOp
from seqthetic.vary.domain_ops import Insert, Remove
from seqthetic.vary.transform import (
    op_to_transform,
    transform_domain,
)
from devtools import debug
from seqthetic.vary.variation import Mixtures, TotalTokenInput, Variation
from seqthetic.utils import generate_id

class Variator:
    spec: SynthesisSpec
    variation: Variation
    _specs: list[SynthesisSpec]

    def __init__(self, spec: SynthesisSpec, variation: Variation):
        self.spec = spec
        self.variation = variation
        self._specs = []
        print(self.variation)
        if self.variation.mixture:
            for mx in self.variation.mixture:
                if len(mx) != len(self.spec.domains):
                    raise ValueError(
                        f"mixture length should be equal to the number of domains"
                    )

    @property
    def specs(self):
        return [self.spec] if len(self._specs) == 0 else self._specs

    @specs.setter
    def specs(self, new_specs):
        self._specs = new_specs

    @staticmethod
    def _normalize_total_token(
        total_token: TotalTokenInput, spec_total_token: int
    ) -> list[int]:
        new_tokens = []
        for token_op in total_token:
            if isinstance(token_op, int):
                new_token = token_op
            else:
                new_token = token_op.compute(spec_total_token)
            new_tokens.append(new_token)

        return new_tokens

    def _vary_total_token(
        self, total_token_input: TotalTokenInput
    ) -> list[SynthesisSpec]:
        new_total_tokens = self._normalize_total_token(
            total_token_input, self.spec.num_token
        )
        new_specs = []
        for total_token, spec in product(new_total_tokens, self.specs):
            new_spec = spec.model_copy(
                deep=True,
                update={
                    "num_token": total_token,
                },
            )

            new_specs.append(new_spec)
        for sp in new_specs:
            sp.update_domain_stat()
        return new_specs

    def _vary_mixture(self, mixtures: Mixtures):
        new_specs = []
        for mixture, spec in product(mixtures, self.specs):
            new_spec = spec.model_copy(deep=True)
            for ratio, domain in zip(mixture, new_spec.domains):
                domain.mixture_ratio = ratio
            new_spec.update_domain_stat()
            new_specs.append(new_spec)
        return new_specs

    def _vary_domain(self, domain_op: ComposeOp):
        new_specs = []
        for spec in self.specs:
            transforms = op_to_transform(spec, domain_op)
            for transform in transforms:
                new_spec = transform_domain(spec, transform)
                new_specs.append(new_spec)
        return new_specs

    def vary(self) -> SpecVariation:
        print("vary method")
        if total_token := self.variation.total_token:
            new_specs = self._vary_total_token(total_token)
            self.specs = new_specs

        if mixtures := self.variation.mixture:
            new_specs = self._vary_mixture(mixtures)
            self.specs = new_specs

        if domain_op := self.variation.domain:
            new_specs = self._vary_domain(domain_op)
            self.specs = new_specs

        if not self.variation.seed.same:
            for spec in self.specs:
                spec.init_seeds(
                    set_domain_seed=self.variation.seed.change_domain,
                    set_vocab_seed=self.variation.seed.change_vocab_noise,
                )
        
        for spec in self.specs:
            spec.id = generate_id()
        return SpecVariation(
            base=self.spec, specs=self.specs, variation=self.variation
        )
