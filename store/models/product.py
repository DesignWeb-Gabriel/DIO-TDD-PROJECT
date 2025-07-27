from store.core.schemas.product import ProductIn
from store.models.base import CreateBaseModel


class ProductModel(ProductIn, CreateBaseModel):
    ...
