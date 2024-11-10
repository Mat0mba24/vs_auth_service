from pydantic import BaseModel


class SService(BaseModel):
    service_id: int
    name: str
