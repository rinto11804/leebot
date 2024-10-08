from type import User, UserJoinedError
from database.connection import DBConnection
from bson import ObjectId
from typing import Optional


class UserQuery:
    def __init__(self, db: DBConnection):
        self.db = db
        self.collection = self.db.get_collection("user")

    def get_user_by_email_and_username(self, email: str, username: str) -> User:
        user = User.from_mongodb(
            self.collection.find_one(
                {"$and": [{"email": email}, {"username": username}]}
            )
        )
        return user

    def add_discord_id(self, user_id: ObjectId, discord_id: str) -> bool:
        user = User.from_mongodb(
            self.collection.find_one(
                {"$and": [{"_id": user_id}, {"discord_id": discord_id}]}
            )
        )
        if user:
            raise UserJoinedError
        res = self.collection.update_one(
            {"_id": user_id},
            {"$set": {"discord_id": discord_id}},
        )

        return res.acknowledged

    def get_user_by_discord_id(self, discord_id: str) -> Optional[User]:
        return User.from_mongodb(self.collection.find_one({"discord_id": discord_id}))
