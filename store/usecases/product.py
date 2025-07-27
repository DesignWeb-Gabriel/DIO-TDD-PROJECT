from typing import List
from uuid import UUID
from datetime import datetime
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorCollection,
)
import pymongo

from store.core.exceptions import NotFoundException
from store.core.schemas.product import (
    ProductIn,
    ProductOut,
    ProductUpdate,
    ProductUpdateOut,
)
from store.db.mongo import db_client
from store.models.product import ProductModel


class ProductUseCase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection: AsyncIOMotorCollection = self.database.get_collection(
            "products"
        )

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())

        # Converter UUID para string e datetime para isoformat para salvar no MongoDB
        product_data = product_model.model_dump()
        product_data["id"] = str(product_data["id"])
        product_data["created_at"] = product_data["created_at"].isoformat()
        product_data["updated_at"] = product_data["updated_at"].isoformat()

        await self.collection.insert_one(product_data)

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        # Buscar pelo campo "id" (não "_id") e converter UUID para string
        result = await self.collection.find_one({"id": str(id)})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        # Converter de volta os tipos corretos
        result["id"] = UUID(result["id"])
        result["created_at"] = datetime.fromisoformat(result["created_at"])
        result["updated_at"] = datetime.fromisoformat(result["updated_at"])

        # Remover o _id do MongoDB se existir
        result.pop("_id", None)

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        result = await self.collection.find().to_list(length=100)

        # Converter de volta os tipos corretos para cada item
        converted_result = []
        for item in result:
            if "id" in item:
                item["id"] = UUID(item["id"])
                item["created_at"] = datetime.fromisoformat(item["created_at"])
                item["updated_at"] = datetime.fromisoformat(item["updated_at"])
                item.pop("_id", None)
                converted_result.append(ProductOut(**item))

        return converted_result

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        from decimal import Decimal
        from bson import Decimal128

        # Preparar dados para atualização, convertendo Decimal para Decimal128
        update_data = body.model_dump(exclude_none=True)
        for key, value in update_data.items():
            if isinstance(value, Decimal):
                update_data[key] = Decimal128(str(value))

        result = await self.collection.find_one_and_update(
            filter={"id": str(id)},
            update={"$set": update_data},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        # Converter de volta os tipos corretos
        result["id"] = UUID(result["id"])
        result["created_at"] = datetime.fromisoformat(result["created_at"])
        result["updated_at"] = datetime.fromisoformat(result["updated_at"])
        # Converter Decimal128 de volta para Decimal
        for key, value in result.items():
            if isinstance(value, Decimal128):
                result[key] = Decimal(str(value))
        result.pop("_id", None)

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": str(id)})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": str(id)})

        return True if result.deleted_count > 0 else False


def get_usecase() -> ProductUseCase:
    return ProductUseCase()


usecase = None  # Será inicializado quando necessário
