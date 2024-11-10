from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.roles import RoleRepo
from src.repositories.services import ServiceRepo
from src.repositories.user_roles import UserRoleRepo
from src.repositories.users import UserRepo


@dataclass
class RequestsRepo:
    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        return UserRepo(self.session)

    @property
    def roles(self) -> RoleRepo:
        return RoleRepo(self.session)

    @property
    def services(self) -> ServiceRepo:
        return ServiceRepo(self.session)

    @property
    def user_roles(self) -> UserRoleRepo:
        return UserRoleRepo(self.session)
