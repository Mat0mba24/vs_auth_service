from src.core.auth import pwd_context
from src.core.config import settings
from src.db.session import session_pool
from src.repositories.requests import RequestsRepo


async def create_superuser():
    async with session_pool() as session:
        repo = RequestsRepo(session)
        if not await repo.users.get_one_or_none(username="supersu"):
            hashed_password = pwd_context.hash(settings.SUPERSU_PASS)
            await repo.users.create(username="supersu", hashed_password=hashed_password)
            await repo.services.create(name="auth")
            await repo.roles.create(name="admin")
            await repo.user_roles.create(
                username="supersu",
                role="admin",
                service="auth"
            )
            await repo.session.commit()
