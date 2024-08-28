from type import Task
from typing import Optional
from bson import ObjectId
from .connection import DBConnection


class TaskQuery:
    def __init__(self, db: DBConnection):
        self.db = db
        self.collection = self.db.get_collection("task")

    def get_task(self, room_id: str, handler: str) -> Optional[Task]:
        task = Task.from_mongodb(
            self.collection.find_one(
                {"$and": [{"handler": handler}, {"room_id": ObjectId(room_id)}]}
            )
        )
        return task

    def is_task_valid(self, room_id: str, handler: str) -> Optional[Task]:
        task = Task.from_mongodb(
            self.collection.find_one(
                {"$and": [{"handler": handler}, {"room_id": ObjectId(room_id)}]}
            )
        )
        if not task:
            return None
        return task
