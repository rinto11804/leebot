from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from enum import Enum


class Roles(Enum):
    ADMIN = "ADMIN"


class UserAlreadyJoinedError(Exception):
    def __init__(self):
        self.message = "User alredy joined the room"
        super().__init__(self.message)


class AnswerAlreadyCorrectedError(Exception):
    def __init__(self):
        self.message = "Answer already corrected"
        super().__init__(self.message)


class AnswerNotFoundError(Exception):
    def __init__(self):
        self.message = "Answer not found"
        super().__init__(self.message)


class User:
    def __init__(
        self,
        id: ObjectId,
        name: str,
        email: str,
        roles: List[str],
        points: int,
        created_at: datetime,
        discord_id: str,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.roles = roles
        self.points = points
        self.created_at = created_at
        self.discord_id = discord_id

    @classmethod
    def from_mongodb(cls, data: dict) -> Optional["User"]:
        if not data:
            return None
        return cls(
            id=data["_id"],
            name=data["name"].strip(),
            email=data["email"],
            roles=data["roles"],
            points=data["points"],
            created_at=data["created_at"],
            discord_id=data.get("discord_id"),
        )

    def __str__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', roles={self.roles})"


class Task:
    def __init__(
        self,
        id: ObjectId,
        title: str,
        handler: str,
        body: str,
        description: str,
        points: int,
        room_id: ObjectId,
        created_at: datetime,
    ):
        self.id = id
        self.title = title
        self.handler = handler
        self.body = body
        self.description = description
        self.points = points
        self.room_id = room_id
        self.created_at = created_at

    @classmethod
    def from_mongodb(cls, data: dict) -> Optional["Task"]:
        if not data:
            return None
        return cls(
            id=data["_id"],
            title=data["title"].strip(),
            handler=data["handler"],
            body=data["body"],
            description=data["description"],
            room_id=data["room_id"],
            points=data["points"],
            created_at=data["created_at"],
        )

    def __str__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', handler='{self.handler}', points={self.points})"


class Answer:
    def __init__(
        self,
        id: ObjectId,
        message_id: str,
        task_id: ObjectId,
        user_id: ObjectId,
        is_correct: bool,
        created_at: datetime,
    ):
        self.id = id
        self.message_id = message_id
        self.task_id = task_id
        self.user_id = user_id
        self.is_correct = is_correct
        self.created_at = created_at

    @classmethod
    def from_mongodb(cls, data: dict) -> Optional["Answer"]:
        if not data:
            return None
        return cls(
            id=data["_id"],
            message_id=data["body"],
            task_id=data["task_id"],
            user_id=data["user_id"],
            is_correct=data["is_correct"],
            created_at=data["created_at"],
        )
