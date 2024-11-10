from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings
from src.repositories.requests import RequestsRepo

engine = create_async_engine(
    settings.construct_sqlalchemy_url,
    pool_size=50,
    max_overflow=20
)

session_pool = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_repo():
    async with session_pool() as session:
        yield RequestsRepo(session)
