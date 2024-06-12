from __future__ import annotations

from typing import ForwardRef, List, Literal

from pydantic import BaseModel, Field

from seqthetic.vary.domain_ops import DomainOp, Vary

ComposeOpRef = ForwardRef("ComposeOp")


class Zip(BaseModel):
    ops: List[ComposeOpRef]  # type: ignore
    op_type: Literal["zip"] = Field(default="zip")


class Product(BaseModel):
    ops: List[ComposeOpRef] # type: ignore
    op_type: Literal["product"] = Field(default="product")


# Define VaryOp after all models are defined
ComposeOp = Zip | Product | DomainOp

# Update ForwardRef type references if necessary (usually not needed in this context)
Zip.model_rebuild()
Product.model_rebuild()


