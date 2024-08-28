from bson import ObjectId
from .connection import DBConnection
import datetime
from type import Answer, AnswerAlreadyCorrectedError, AnswerNotFoundError


class AnswerQuery:
    def __init__(self, db: DBConnection):
        self.db = db
        self.collection = self.db.get_collection("answer")

    def create_answer(
        self, message_id: str, task_id: ObjectId, user_id: ObjectId
    ) -> bool:
        if self.collection.find_one(
            {"$and": [{"user_id": user_id}, {"task_id": task_id}]}
        ):
            return False
        answer = self.collection.insert_one(
            {
                "body": message_id,
                "task_id": task_id,
                "user_id": user_id,
                "is_correct": False,
                "created_at": datetime.datetime.now(),
            }
        )
        return answer.acknowledged

    def mark_answer_as_correct(self, message_id: str, user_id: ObjectId):
        answer = Answer.from_mongodb(
            self.collection.find_one(
                {"$and": [{"body": message_id, "user_id": user_id}]}
            )
        )
        if not answer:
            raise AnswerNotFoundError
        if answer.is_correct:
            raise AnswerAlreadyCorrectedError
        res = self.collection.update_one(
            {"$and": [{"body": message_id, "user_id": user_id}]},
            {"$set": {"is_correct": True}},
        )
        return res.acknowledged
