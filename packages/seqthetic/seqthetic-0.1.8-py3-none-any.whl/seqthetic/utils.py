import re
from typing import Annotated

import numpy as np
from nanoid import generate
from pydantic import BaseModel, BeforeValidator, Field


_size_pattern = re.compile(r"[0-9]+(?:\.[0-9]+)?[BMK]")
_id_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
generate_id = lambda: generate(alphabet=_id_alphabet, size=10)
ID = Field(default_factory=generate_id)


def validate_size_value(v):
    if isinstance(v, str):
        v = v.upper()
        scale = 0
        if _size_pattern.match(v):
            if v.endswith("B"):
                scale = 1000000000
            elif v.endswith("M"):
                scale = 1000000
            elif v.endswith("K"):
                scale = 1000
            else:
                raise ValueError("invalid size format")
            return float(v[:-1]) * scale

    elif isinstance(v, int):
        return v
    else:
        raise TypeError("string or integer required")


SizeValue = Annotated[str | int, BeforeValidator(validate_size_value)]


class MyModel(BaseModel):
    size: SizeValue


def make_digitizer(ratio: float):
    # 从最大到最小值均分
    def digitize(arr):
        bin_count = round(len(arr) // ratio)
        bins = np.linspace(arr.max(), arr.min(), bin_count)[1:-1]
        return np.digitize(arr, bins)

    return digitize


