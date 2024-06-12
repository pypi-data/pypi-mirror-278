import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import namedtuple
from seqthetic.synthesis_spec import SynthesisSpec

SavePath = namedtuple("SavePath", ["spec_path", "dataset_path"])


class Dataset:
    df: pd.DataFrame
    spec: SynthesisSpec
    columns = ["dependency", "sequence", "domain_id", "split", "metadata"]
    dtype = {
        "dependency": object,
        "sequence": object,
        "split": str,
        "domain_id": str,
        "metadata": object,
    }

    def __init__(self, spec: SynthesisSpec, df: pd.DataFrame):
        self.spec = spec
        self.df = df

    def save(self, path: str, format="csv"):
        if format == "csv":
            spec_path = self.spec.save(path)
            save_name = self.spec.name or self.spec.id

            dataset_path = Path(path) / f"{save_name}.csv"
            print(f"Save the dataset to {dataset_path}")
            self.df["metadata"] = self.df["metadata"].apply(json.dumps)
            self.df.to_csv(dataset_path, index=False)
            return SavePath(spec_path=spec_path, dataset_path=str(dataset_path))
        else:
            raise NotImplementedError("Only csv format is supported")

    def view_dependencies(self, n=1):
        assert n > 0 and n <= 9, "n should be between 1 and 9"
        num_dep = min(n, len(self.df["dependency"]))

        rows = cols = 3
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=[f"Dependency {i+1}" for i in range(num_dep)],
        )

        for i in range(num_dep):
            dep = self.df["dependency"].iloc[i]
            row, col = (i // cols) + 1, (i % cols) + 1
            fig.add_trace(
                go.Scatter(x=list(range(len(dep))), y=dep, mode="markers"),
                row=row,
                col=col,
            )

        fig.update_layout(height=1200, width=1200, title_text="Dependencies Overview")
        fig.show()

    @classmethod
    def load_csv(cls, path: str, name=""):
        df_path = Path(path) / f"{name}.csv"
        spec_path = Path(path) / f"{name}.synspec.json"
        df = pd.read_csv(df_path, dtype=cls.dtype)
        df["dependency"] = df["dependency"].apply(json.loads)
        df["sequence"] = df["sequence"].apply(json.loads)
        df["metadata"] = df["metadata"].apply(json.loads)
        spec = SynthesisSpec.load(spec_path)
        return cls(spec, df)

    @classmethod
    def load_sqlite(cls, path: str):
        raise NotImplementedError("Not implemented yet")

    def __getitem__(self, item):
        return self.df[item]

    def __getattr__(self, item):
        attr = getattr(self.df, item)
        if callable(attr):
            return attr
        else:
            raise AttributeError(
                f"'{type(self).__name__}' object has no attribute '{item}'"
            )
