import json
from pathlib import Path
from typing import Literal, TypeVar
from pydantic import BaseModel, Field
from seqthetic.dataset import Dataset
from seqthetic.synthesis_spec import SynthesisSpec
from seqthetic.synthesizer import Synthesizer
from seqthetic.utils import generate_id
from seqthetic.vary.variation import Variation


class SpecVariationDTO(BaseModel):
    base: str | SynthesisSpec
    specs: list[str] | list[SynthesisSpec]
    datasets: list[str]
    variation: Variation
    diff: dict | None = None  # todo


class SpecVariation:
    id: str
    base: SynthesisSpec
    specs: list[SynthesisSpec]
    datasets: list[Dataset]
    made_datasets: bool
    base_path: str | None = None
    variation: Variation
    diff: dict | None = None  # todo

    def __init__(
        self,
        base: SynthesisSpec,
        specs: list[SynthesisSpec],
        variation: Variation,
        diff: dict | None = None,
    ):
        self.id = generate_id()
        self.base = base
        self.specs = specs
        self.datasets = []
        self.made_datasets = False
        self.variation = variation
        self.diff = diff

    def generate(self):
        if self.made_datasets:
            return self
        self.datasets = [Synthesizer(spec).make_dataset() for spec in self.specs]
        return self

    @staticmethod
    def load(variation_path: str):
        variation_path_obj = Path(variation_path)

        if not variation_path_obj.exists():
            raise FileNotFoundError(f"{variation_path} does not exist")

        spec_variation_dct = json.loads(variation_path_obj)
        dto = SpecVariationDTO.model_validate(spec_variation_dct)
        base_path = Path(dto.base)
        specs_path = [Path(spec) for spec in dto.specs]
        dataset_paths = [Path(dataset) for dataset in dto.datasets]
        base_spec = SynthesisSpec.model_validate(json.load(base_path))
        specs = [SynthesisSpec.model_validate(json.load(spec)) for spec in specs_path]
        datasets = [Dataset.load_csv(dataset) for dataset in dataset_paths]
        return SpecVariation(
            base=base_spec,
            specs=specs,
            datasets=datasets,
            variation=dto.variation,
            diff=dto.diff,
        )

    def save(
        self,
        variation_path: str,
        spec_form: Literal["path", "object"] = "path",
        path_mode: Literal["separate", "together"] = "separate",
        dataset_format: Literal["csv"] = "csv",
        dataset_path: str | None = None,
        name: str | None = None,
    ):
        """
        spec_form means whether the spec in the group file is saved as complete object or file path.
        save_mode means whether the datasets and groups are saved in separate directoies or in a single directory.
        if save_mode is separate, please specify both group_path and dataset_path.
        if save_mode is together, please only specify path.
        """

        if path_mode == "separate":
            assert (
                dataset_path
            ), "dataset_path must be specified when path_mode is separate"

        main_dataset_path = dataset_path or variation_path

        save_object = spec_form == "object"
        base = self.base.save(main_dataset_path) if spec_form == "path" else self.base
        specs = self.specs if save_object else []

        dataset_paths = []
        for dataset in self.datasets:
            spec_path, dataset_path = dataset.save(main_dataset_path, dataset_format)
            dataset_paths.append(dataset_path)
            if spec_form == "path":
                specs.append(spec_path)
        dto = SpecVariationDTO(
            base=base, specs=specs, datasets=dataset_paths, variation=self.variation
        )
        dto_json = dto.model_dump_json(indent=4)
        variation_path_obj = Path(variation_path) / f"{name or self.id}.specvar.json"
        with open(variation_path_obj, "w") as f:
            f.write(dto_json)
