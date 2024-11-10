from typing import Optional

from pydantic import BaseModel


class SUser(BaseModel):
    user_id: int
    username: str
    email: Optional[str] = None
    hashed_password: str


class SCreateUser(BaseModel):
    username: str
    password: str
