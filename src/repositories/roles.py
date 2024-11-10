from src.models.roles import Role
from src.repositories.base import BaseRepo


class RoleRepo(BaseRepo):
    model = Role
