from pydantic import BaseModel


class SRole(BaseModel):
    role_id: int
    name: str
