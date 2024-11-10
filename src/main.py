from fastapi import FastAPI

from src.api.routers import all_routers
from src.utils.create_superuser import create_superuser


async def lifespan(_: FastAPI):
    await create_superuser()
    yield


app = FastAPI(
    title="Центральный сервис авторизации",
    lifespan=lifespan
)

for router in all_routers:
    app.include_router(router)
