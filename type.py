from datetime import datetime
from typing import List, Optional
from bson import ObjectId


class UserAlreadyJoinedError(Exception):
    def __init__(self):
        self.message = "User alredy joined the room"
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
        discord_id: Optional[str] = None,
        password: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.email = email
        self.roles = roles
        self.points = points
        self.created_at = created_at
        self.discord_id = discord_id
        self.password = password

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
            password=data.get("password"),
        )

    def __str__(self) -> str:
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', roles={self.roles})"
