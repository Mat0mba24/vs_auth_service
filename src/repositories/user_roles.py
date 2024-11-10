from sqlalchemy import text

from src.models import UserRole
from src.repositories.base import BaseRepo


class UserRoleRepo(BaseRepo):
    model = UserRole

    async def is_exists(
            self,
            **params
    ) -> bool:
        query = text(
            """
            SELECT EXISTS (
                SELECT 1
                FROM user_roles
                WHERE 
                    user_id = (SELECT user_id FROM users WHERE username = :username)
                    AND service_id = (SELECT service_id FROM services WHERE name = :service)
                    AND role_id = (SELECT role_id FROM roles WHERE name = :role)
            )
            """
        )
        result = await self.session.execute(
            statement=query,
            params=params
        )
        return result.scalar()

    async def create(
            self,
            **params
    ) -> None:
        query = text(
            """
            INSERT INTO user_roles (user_id, service_id, role_id)
            VALUES (
                (SELECT user_id FROM users WHERE username = :username),
                (SELECT service_id FROM services WHERE name = :service),
                (SELECT role_id FROM roles WHERE name = :role)
            )
            ON CONFLICT DO NOTHING;
            """
        )
        await self.session.execute(
            statement=query,
            params=params
        )
        await self.session.commit()
