from typing import Annotated, Optional
from decimal import Decimal
from bson import Decimal128
from pydantic import AfterValidator, BaseModel, Field

from store.core.schemas.base import BaseSchemaMixin, OutMixin


class ProductBase(BaseModel):
    name: str = Field(
        ..., description="The name of the product", min_length=3, max_length=100
    )
    quantity: int = Field(..., description="The quantity of the product", gt=0)
    price: Decimal = Field(..., description="The price of the product", gt=0)
    status: bool = Field(..., description="The status of the product")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...


class ProductOut(ProductIn, OutMixin):
    ...


def convert_decimal_128(v):
    return Decimal128(str(v))


Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]


class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")


class ProductUpdateOut(ProductUpdate, OutMixin):
    ...
