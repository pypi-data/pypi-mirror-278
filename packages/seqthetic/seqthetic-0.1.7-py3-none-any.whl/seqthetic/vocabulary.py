import logging
from abc import ABC, abstractmethod
from typing import Dict, Literal, Optional, Union

import numpy as np
from pydantic import BaseModel, Field, computed_field, field_validator

from seqthetic.range import Range
from seqthetic.seed import Seed


class VocabProb:
    _arr: np.ndarray

    def __init__(self, size: int, word: np.ndarray, prob: np.ndarray):
        self._arr = np.zeros(size, dtype=[("word", np.int32), ("prob", np.float32)])
        self._arr["word"] = word
        self._arr["prob"] = prob

    @property
    def word(self):
        return self._arr["word"]

    @property
    def prob(self):
        return self._arr["prob"]

    def sample_vocab(
        self,
        seq_vocab_size: int,
        rng: np.random.Generator = np.random.default_rng(),
        sample_by_frequency=True,
        sort_by_frequency=True,
    ) -> np.ndarray:
        p = self.prob if sample_by_frequency else None
        try:
            sampled_unsorted = rng.choice(
                self._arr, size=seq_vocab_size, replace=False, p=p
            )
        except:
            logging.error(f"_arr_size: {len(self._arr)}, seq_vocab: {seq_vocab_size}")
            raise
        if sort_by_frequency:
            # 获取按照prob降序排序的索引
            pos_vocab_sort_indices = np.argsort(-sampled_unsorted["prob"])
            # 使用索引对vocab_prob重新排序
            sampled_vocab = sampled_unsorted[pos_vocab_sort_indices]
            return sampled_vocab["word"]
        else:
            np.shuffle(sampled_unsorted)
            sampled_vocab = sampled_unsorted

        return sampled_vocab["word"]


class DistributionNoise(BaseModel):
    """noise for vocabulary distribution"""

    type: Literal["multiplicative", "additive"]
    level: float

    def add_noise(self, vocab_prob: VocabProb, rng: np.random.Generator) -> VocabProb:
        noise = rng.normal(0, self.level, len(vocab_prob))
        if self.type == "additive":
            vocab_prob.prob += noise
        else:
            vocab_prob.prob *= noise

        # normalize prob
        vocab_prob.prob = vocab_prob.prob / np.sum(vocab_prob.prob)
        return vocab_prob


class BaseVocabulary(BaseModel, ABC):
    size: int
    noise: Optional[DistributionNoise] = None
    seed: Seed = Field(default_factory=Seed, exclude=True)
    base_seed_schema: list[str] = Field(
        default_factory=lambda: ["sample", "noise"], exclude=True
    )
    custom_seed_schema: list[str] = Field(default_factory=list, exclude=True)

    @property
    def seed_schema(self) -> list[str]:
        return self.base_seed_schema + self.custom_seed_schema

    def make_vocabulary(self) -> VocabProb:
        vocab_prob = self.make_vocab_prob()
        if not self.noise:
            return vocab_prob
        else:
            noise_rng = self.seed.get_rng("noise")
            return self.noise.add_noise(vocab_prob, self, noise_rng)

    @abstractmethod
    def make_vocab_prob(self) -> VocabProb:
        pass

    def set_seed(self, seed: Seed):
        self.seed = seed


# todo
class CorpusVocabulary(BaseVocabulary):
    distribution: str = "corpus"
    weight: Dict[int, float]
    corpus_name: str

    def make_vocab_prob(self) -> VocabProb:
        vocab_prob = VocabProb(
            self.size, list(self.weight.keys()), list(self.weight.values())
        )
        return vocab_prob


class LogLinearVocabulary(BaseVocabulary):
    """todo"""

    distribution: str = "loglinear"

    def make_vocab_prob(self) -> VocabProb:
        raise NotImplementedError("loglinear vocabulary is not implemented")


class ZipfVocabulary(BaseVocabulary):
    distribution: str = "zipf"
    alpha: float = 1
    beta: float = 2.7

    def make_vocab_prob(self) -> VocabProb:
        vocab = np.arange(self.size)
        freq = 1 / (vocab + 1 + self.beta)
        prob = freq / np.sum(freq)
        vocab_prob = VocabProb(self.size, vocab, prob)

        return vocab_prob


class UniformVocabulary(BaseVocabulary):
    distribution: str = "uniform"

    def make_vocab_prob(self) -> VocabProb:
        vocab = np.arange(self.size)
        vocab_prob = VocabProb(self.size, vocab, np.full(self.size, 1 / self.size))
        return vocab_prob

# todo: use a genral Vocabulary class.
VocabularySpec = Union[
    ZipfVocabulary, UniformVocabulary, CorpusVocabulary, LogLinearVocabulary
]
