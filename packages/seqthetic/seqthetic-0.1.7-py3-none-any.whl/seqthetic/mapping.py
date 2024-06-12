from typing import Callable, Dict, List, Literal, Tuple

from tqdm import tqdm
import numpy as np
from pydantic import BaseModel, Field

from seqthetic.seed import Seed
from seqthetic.vocabulary import VocabProb
from joblib_progress import joblib_progress
from joblib import Parallel, delayed
from more_itertools import chunked

Mapping = Dict[int, Tuple[List[int], List[float]]]


class MappingSpec(BaseModel):
    """Mapping dependency to word"""

    sample_by: Literal["frequency", "random"] = "frequency"
    map_by: Literal["frequency", "random"] = "frequency"
    # whether to split dependency and generate multiple sequences
    # e.g. 1 means no split
    # 2 means 1 dependency split in half and mapped to 2 sequences
    #
    # todo
    split_dependency_ratio: int = Field(default=1, ge=1)
    # how many sequence are generated from the same dependency with different vocabulary
    # e.g. 1 means no duplication, 2 means 1 dependency mapped to 2 sequences with different vocabulary
    # todo
    duplicate_dependency_ratio: int = Field(default=1, ge=1)

    @staticmethod
    def make_dep_freq(dependency: np.ndarray) -> np.ndarray:
        # 定义结构体的数据类型
        dtype = [("dep", int), ("freq", int)]

        # 统计每个元素的出现频率
        unique_deps, counts = np.unique(dependency, return_counts=True)

        # 创建结构体数组
        structured_array = np.array(list(zip(unique_deps, counts)), dtype=dtype)

        # 按频率降序排列
        sorted_array = np.sort(structured_array, order="freq")[::-1]

        return sorted_array["dep"]

    @staticmethod
    def map_one_to_sequence(
        dependency: np.ndarray,
        unique_dep: np.ndarray,
        sampled_vocab: np.ndarray,
    ):
        # consider moving mapping to prepare_params
        mapping = {d: v for d, v in zip(unique_dep, sampled_vocab)}
        seq = np.array([mapping[d] for d in dependency])
        return seq

    def prepare_params(
        self,
        dependencies: list[np.ndarray],
        vocab: VocabProb,
        sample_rngs: list[np.random.Generator],
        n_jobs: int,
        unique_dep_str: str,
        sample_str: str,
    ):
        sample_by = self.sample_by == "frequency"
        map_by = self.map_by == "frequency"
        with joblib_progress(
            unique_dep_str, total=len(dependencies)
        ):
            unique_deps = list(
                Parallel(n_jobs=n_jobs)(
                    delayed(self.make_dep_freq)(dependency)
                    for dependency in dependencies
                )
            )
        # sampled vocabs is much smaller than vocabs
        dep_vocab_nums = [len(dep_freq) for dep_freq in unique_deps]
        with joblib_progress(
            sample_str, total=len(dependencies)
        ):
            sampled_vocabs = list(
                Parallel(n_jobs=n_jobs)(
                    delayed(vocab.sample_vocab)(
                        dep_vocab_num,
                        rng,
                        sample_by_frequency=sample_by,
                        sort_by_frequency=map_by,
                    )
                    for dep_vocab_num, rng in zip(dep_vocab_nums, sample_rngs)
                )
            )

        return unique_deps, sampled_vocabs

    def map_to_sequence(
        self, dependencies: list[np.ndarray], vocab: VocabProb, vocab_seed: Seed
    ) -> list[list[int]]:
        num_dependency = len(dependencies)

        sample_rngs = vocab_seed.get_rng("sample", num_dependency, return_list=True)

        dep_freqs = [
            self.make_dep_freq(dependency)
            for dependency in tqdm(dependencies, desc="Dependency to vocab mapping.")
        ]
        #
        # one to one mapping from dependency to vocab, on condition that it's used for sequence
        dep_vocab_nums = [len(dep_freq) for dep_freq in dep_freqs]

        sample_by = self.sample_by == "frequency"
        map_by = self.map_by == "frequency"

        sampled_vocabs = [
            vocab.sample_vocab(
                dep_vocab_num,
                rng,
                sample_by_frequency=sample_by,
                sort_by_frequency=map_by,
            )
            for dep_vocab_num, rng in zip(dep_vocab_nums, sample_rngs)
        ]

        seqs = []
        for dependency, dep_freq, sampled_vocab in zip(
            dependencies, dep_freqs, sampled_vocabs
        ):
            unique_dep = dep_freq["dep"]
            mapping = {d: v for d, v in zip(unique_dep, sampled_vocab)}
            seq = [mapping[d] for d in dependency]
            seqs.append(seq)

        return seqs
