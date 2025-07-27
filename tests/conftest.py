import pytest
import pytest_asyncio
import asyncio
import sys
from uuid import UUID

from store.core.schemas.product import ProductIn, ProductUpdate
from tests.factories import product_data, products_data

# Configuração específica para Windows para evitar problemas com ProactorEventLoop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def client():
    from store.main import app
    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def products_url() -> str:
    return "/products/"


@pytest.fixture
def product_id() -> UUID:
    return UUID("fce6cc37-10b9-4a8e-a8b2-977df327001a")


@pytest.fixture
def product_in():
    return ProductIn(**product_data())


@pytest.fixture
def product_update(product_id):
    return ProductUpdate(**product_data(), id=product_id)


@pytest.fixture
def isolated_product_usecase():
    """Retorna uma nova instância isolada do ProductUseCase para testes"""
    from motor.motor_asyncio import AsyncIOMotorClient
    from store.core.config import settings
    from store.usecases.product import ProductUseCase

    class IsolatedProductUseCase(ProductUseCase):
        def __init__(self):
            self.client = AsyncIOMotorClient(settings.MONGO_URL)
            self.database = self.client.get_database()
            self.collection = self.database.get_collection("products")

    return IsolatedProductUseCase()


@pytest_asyncio.fixture
async def product_inserted(isolated_product_usecase, product_in):
    return await isolated_product_usecase.create(body=product_in)


@pytest.fixture
def products_in():
    return [ProductIn(**product) for product in products_data()]


@pytest_asyncio.fixture
async def products_inserted(isolated_product_usecase, products_in):
    return [
        await isolated_product_usecase.create(body=product_in)
        for product_in in products_in
    ]
