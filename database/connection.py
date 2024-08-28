import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


class DBConnection:
    def __init__(self):
        MONGODB_URI: str = str(os.getenv("MONGODB_URI"))
        self.client = MongoClient(MONGODB_URI)
        self.db: Database = self.client.get_database("decode")

    def get_collection(self, colllection_name: str) -> Collection:
        return self.db.get_collection(colllection_name)
