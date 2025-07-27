from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from store.core.config import settings


class MongoClient:
    def __init__(self) -> None:
        self.client = AsyncIOMotorClient(settings.MONGO_URL)

    def get(self) -> AsyncIOMotorClient:
        return self.client

    def get_database(self) -> AsyncIOMotorDatabase:
        return self.client.get_database("store")


db_client = MongoClient()
