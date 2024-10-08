import datetime
from bson import ObjectId
from database.connection import DBConnection


class RoomQuery:
    def __init__(self, db: DBConnection):
        self.db = db
        self.room_collection = self.db.get_collection("room")
        self.room_join_collection = self.db.get_collection("room_joinlist")

    def join_room(self, room_id: str, user_id: ObjectId) -> bool:
        joined = self.room_join_collection.find_one(
            {"$and": [{"room_id": ObjectId(room_id)}, {"user_id": user_id}]}
        )
        if joined:
            return False
        res = self.room_join_collection.insert_one(
            {
                "room_id": ObjectId(room_id),
                "user_id": user_id,
                "points": 0,
                "created_at": datetime.datetime.now(),
            }
        )
        return res.acknowledged

    def generate_leaderboard(self, room_id: str):
        pipeline = [
            {"$match": {"room_id": ObjectId(room_id)}},
            {
                "$lookup": {
                    "from": "user",
                    "localField": "user_id",
                    "foreignField": "_id",
                    "as": "user",
                }
            },
            {"$unwind": "$user"},
            {
                "$group": {
                    "_id": "$_id",
                    "user_id": {"$first": "$user_id"},
                    "username": {"$first": "$user.name"},
                    "points": {"$sum": "$points"},
                }
            },
            {"$sort": {"points": -1}},
        ]

        result = self.room_join_collection.aggregate(pipeline)
        return list(result)

    def grant_point(self, room_id: str, user_id: str, point: int):
        room_join = self.room_join_collection.update_one(
            {"$and": [{"room_id": ObjectId(room_id)}, {"user_id": user_id}]},
            {"$inc": {"points": int(point)}},
        )

        return room_join.acknowledged
