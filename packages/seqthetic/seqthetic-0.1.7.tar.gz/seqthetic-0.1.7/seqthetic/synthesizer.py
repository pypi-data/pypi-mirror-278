import logging

from more_itertools import chunked
import pandas as pd
from tqdm import tqdm
from seqthetic.dataset import Dataset

from .synthesis_spec import DomainSpec, SynthesisSpec
from pydantic import BaseModel
import random
from joblib import Parallel, delayed
from joblib_progress import joblib_progress
import gc


class DomainItem(BaseModel):
    dependency: list[int]
    sequence: list[int]
    domain_id: str
    metadata: dict
    split: str = "train"


class DomainResult(BaseModel):
    items: list[DomainItem]


class Synthesizer:
    """
    spec: SynthesisSpec
    n_jobs: number of processes. pass -1 to use all cpus (large may take up large amounts of memory)
    """

    def __init__(self, spec: SynthesisSpec, n_jobs=4, chunk_size=25000):
        self.spec = spec
        self.n_jobs = n_jobs
        self.chunk_size = chunk_size
        self.vocab_prob = spec.vocabulary.make_vocabulary()
        self.dataset = pd.DataFrame(columns=Dataset.columns)
        self.made_dataset = False

    def make_dataset(self, debug=False) -> Dataset:
        # todo: progress bar
        if self.made_dataset:
            return self.dataset
        if debug:
            logging.basicConfig(level=logging.DEBUG)

        total = len(self.spec.domains)
        domains: list[DomainResult] = [
            self._make_domain(domain, i, total, debug)
            for i, domain in enumerate(self.spec.domains)
        ]
        items = self._dataset_train_test_split(domains)
        self.dataset = pd.DataFrame.from_records(
            [item.model_dump() for item in items], columns=Dataset.columns
        )
        self.made_dataset = True
        return Dataset(self.spec, self.dataset)

    def _shuffle(self, seed_name: str, lst: list):
        rng = self.spec.seeds.split.get_rng(seed_name)

        rng.shuffle(lst)

    def _domain_split(self, items: list[DomainItem]):
        train_index, val_index = self.spec.split.get_index(len(items))
        for item in items[train_index:val_index]:
            item.split = "val"
        for item in items[val_index:]:
            item.split = "test"

    def _make_domain(
        self, domain: DomainSpec, i: int, total: int, debug=False
    ) -> DomainResult:
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        print(f"Synthesizing data for domain {i+1}/{total}")
        print(
            f"\tMixture ratio: {domain.mixture_ratio}, Num_sequence: {domain.num_sequence}"
        )
        print(f"\tSequence length: {domain.dependency.sequence_length}")
        print(f"\tDependency: {type(domain.dependency).__name__}")
        print(f"\tDependency parameters: {domain.dependency.report_param()}")

        num_seq = domain.num_sequence
        dep_params, metadata = domain.dependency.prepare_params(num_seq)

        with joblib_progress("Making dependencies", total=num_seq):
            dependencies = list(
                Parallel(n_jobs=self.n_jobs)(
                    delayed(domain.dependency.make_one_dependency)(param)
                    for param in dep_params
                ),
            )

        chunk_size = self.chunk_size
        num_chunk = num_seq // chunk_size + 1
        metadata_chunks = chunked(metadata, chunk_size)
        dep_chunks = chunked(dependencies, chunk_size)
        sample_rngs = self.spec.vocabulary.seed.get_rng(
            "sample", num_seq, return_list=True
        )
        sample_rng_chunks = chunked(sample_rngs, chunk_size)
        domain_items = []
        domain_id = domain.id
        unique_dep_str = "Getting Unique Dependencies"
        mapping_str = "Mapping dependencies with vocabularies"
        pack_domain_item = "Packing domain items"
        sample_str = "Sampling Vocabs"
        strs = [unique_dep_str, mapping_str, pack_domain_item, sample_str]
        for i, (dep_chunk, metadata_chunk, sample_rng_chunk) in enumerate(
            zip(dep_chunks, metadata_chunks, sample_rng_chunks)
        ):
            chunk_prefix = f"Chunk {i + 1} / {num_chunk}"

            
            
            strs = [f"{chunk_prefix}: {s}" for s in strs]
            max_len = max([len(s) for s in strs])
            ljusted = [s.ljust(max_len) for s in strs]
            unique_dep_str, mapping_str, pack_domain_item, sample_str = ljusted

            unique_deps, sampled_vocabs = domain.mapping.prepare_params(
                dep_chunk,
                self.vocab_prob,
                sample_rng_chunk,
                self.n_jobs,
                unique_dep_str,
                sample_str,
            )

            with joblib_progress(
                mapping_str,
                total=len(dep_chunk),
            ):
                sequences = list(
                    Parallel(n_jobs=self.n_jobs)(
                        delayed(domain.mapping.map_one_to_sequence)(
                            dependency, unique_dep, sampled_vocab
                        )
                        for dependency, unique_dep, sampled_vocab in zip(
                            dep_chunk, unique_deps, sampled_vocabs
                        )
                    )
                )
            with joblib_progress(
                pack_domain_item,
                total=len(dep_chunk),
            ):
                domain_item_chunk = list(
                    Parallel(n_jobs=self.n_jobs)(
                        delayed(DomainItem)(
                            dependency=dep,
                            sequence=seq,
                            domain_id=domain_id,
                            metadata=meta,
                        )
                        for dep, seq, meta in zip(dep_chunk, sequences, metadata_chunk)
                    )
                )
                domain_items.extend(domain_item_chunk)

        return DomainResult(items=domain_items)

    def _dataset_train_test_split(self, domains: list[DomainResult]):
        split_config = self.spec.split
        print(f"Split data with the config: {split_config}")
        items = []

        if split_config.shuffle_dataset:
            items = [item for domain in domains for item in domain.items]
            self._shuffle("shuffle_dataset", items)
            self._domain_split(items)
        else:
            if split_config.shuffle_domain_order:
                self._shuffle("shuffle_domain_order", domains)
            if split_config.shuffle_domain_sequence:
                rngs = self.spec.seeds.split.get_rng(
                    "shuffle_domain_sequence", len(domains), return_list=True
                )
                for rng, domain in zip(rngs, domains):
                    rng.shuffle(domain.items)
            for domain in domains:
                self._domain_split(domain.items)
                items.extend(domain.items)
        return items

    def save_dataset(self, path: str = "./"):
        if not self.made_dataset:
            raise ValueError("dataset not made yet")
        Dataset(self.spec, self.dataset).save(path)
