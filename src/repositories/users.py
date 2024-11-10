from src.models.users import User
from src.repositories.base import BaseRepo


class UserRepo(BaseRepo):
    model = User
