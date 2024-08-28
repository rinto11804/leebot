from type import User
from database.connection import DBConnection
from bson import ObjectId


class UserQuery:
    def __init__(self):
        self.db = DBConnection()
        self.collection = self.db.get_collection("user")

    def get_user_by_email(self, email: str) -> User:
        user = User.from_mongodb(self.collection.find_one({"email": email}))
        return user

    def add_discord_id(self, user_id: ObjectId, discord_id: str) -> bool:
        user = User.from_mongodb(self.collection.find_one({"_id": user_id}))
        if user.discord_id != "":
            return False
        res = self.collection.update_one(
            {"_id": user_id},
            {"$set": {"discord_id": discord_id}},
        )

        return res.acknowledged

    def get_user_by_discord_id(discord_id: str) -> User:
        pass
