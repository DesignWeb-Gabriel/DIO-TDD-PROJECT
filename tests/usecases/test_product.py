from typing import List
import pytest
from uuid import UUID
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from store.core.exceptions import NotFoundException
from store.core.schemas.product import ProductOut, ProductUpdateOut
from store.core.config import settings


class ProductUseCaseForTesting:
    def __init__(self) -> None:
        # Criar um cliente MongoDB completamente novo para cada instância
        self.client = AsyncIOMotorClient(settings.MONGO_URL)
        self.database = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body):
        from store.models.product import ProductModel
        from store.core.schemas.product import ProductOut

        product_model = ProductModel(**body.model_dump())

        # Converter UUID para string e datetime para isoformat para salvar no MongoDB
        product_data = product_model.model_dump()
        product_data["id"] = str(product_data["id"])
        product_data["created_at"] = product_data["created_at"].isoformat()
        product_data["updated_at"] = product_data["updated_at"].isoformat()

        await self.collection.insert_one(product_data)
        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID):
        from datetime import datetime

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

    async def query(self):
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

    async def update(self, id: UUID, body):
        import pymongo

        # Preparar os dados para atualização
        update_data = body.model_dump(exclude_none=True)
        if "updated_at" in update_data:
            update_data["updated_at"] = update_data["updated_at"].isoformat()

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
        result.pop("_id", None)

        return ProductUpdateOut(**result)


@pytest.mark.asyncio
async def test_usecases_should_return_success(product_in):
    # Criar uma nova instância do usecase para este teste
    product_usecase = ProductUseCaseForTesting()
    result = await product_usecase.create(body=product_in)

    assert isinstance(result, ProductOut)
    assert isinstance(result.id, UUID)
    assert isinstance(result.created_at, datetime)
    assert isinstance(result.updated_at, datetime)
    assert result.name == product_in.name
    assert result.quantity == product_in.quantity
    assert result.price == product_in.price
    assert result.status == product_in.status


@pytest.mark.asyncio
async def test_usecases_get_should_return_success(product_in):
    # Criar uma nova instância do usecase para este teste
    product_usecase = ProductUseCaseForTesting()

    # Primeiro criar um produto
    created_product = await product_usecase.create(body=product_in)

    # Depois buscar o produto criado
    result = await product_usecase.get(id=created_product.id)

    assert isinstance(result, ProductOut)
    assert isinstance(result.id, UUID)
    assert result.id == created_product.id
    assert result.name == created_product.name
    assert result.quantity == created_product.quantity
    assert result.price == created_product.price
    assert result.status == created_product.status


@pytest.mark.asyncio
async def test_usecases_get_should_not_found(product_id, isolated_product_usecase):
    with pytest.raises(NotFoundException) as err:
        await isolated_product_usecase.get(id=product_id)

    assert err.value.message == f"Product not found with filter: {product_id}"


@pytest.mark.asyncio
async def test_usecases_query_should_return_success(isolated_product_usecase):
    result = await isolated_product_usecase.query()

    assert isinstance(result, List)


@pytest.mark.asyncio
async def test_usecases_update_should_return_success(
    product_inserted, product_update, isolated_product_usecase
):
    # Depois atualizar o produto criado
    from decimal import Decimal

    product_update.price = Decimal("7.500")
    result = await isolated_product_usecase.update(
        id=product_inserted.id, body=product_update
    )

    assert isinstance(result, ProductUpdateOut)


@pytest.mark.asyncio
async def test_usecases_delete_should_return_success(
    product_inserted, isolated_product_usecase
):
    result = await isolated_product_usecase.delete(id=product_inserted.id)

    assert result is True


@pytest.mark.asyncio
async def test_usecases_delete_should_not_found(product_id, isolated_product_usecase):
    with pytest.raises(NotFoundException) as err:
        await isolated_product_usecase.delete(id=product_id)

    assert err.value.message == f"Product not found with filter: {product_id}"
