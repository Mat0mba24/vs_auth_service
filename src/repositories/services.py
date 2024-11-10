from src.models.services import Service
from src.repositories.base import BaseRepo


class ServiceRepo(BaseRepo):
    model = Service
