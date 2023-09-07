import hashlib
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    password_hash: str
    is_admin: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def from_tuple(cls, user_tuple):
        return cls(
            id=user_tuple[0],
            username=user_tuple[1],
            email=user_tuple[2],
            password_hash=user_tuple[3],
            is_admin=user_tuple[4],
            created_at=user_tuple[5],
            updated_at=user_tuple[6],
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Get the password hash."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def tuple(self, return_password=False):
        if return_password:
            return (
                self.id,
                self.username,
                self.email,
                self.password_hash,
                self.is_admin,
                self.created_at,
                self.updated_at,
            )
        return (
            self.id,
            self.username,
            self.email,
            self.is_admin,
            self.created_at,
            self.updated_at,
        )
