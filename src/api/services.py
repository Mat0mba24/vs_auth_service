from typing import List

from fastapi import APIRouter, Depends, status

from src.api.dependencies import is_admin
from src.core.logger import logger
from src.db.session import get_repo
from src.exceptions.custom_exceptions import CannotAddDataToDatabase, CannotDeleteDataFromDatabase
from src.repositories.requests import RequestsRepo
from src.schemas.services import SService

services_router = APIRouter(
    prefix="/services",
    tags=["Сервисы"]
)


@services_router.post(
    "",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_201_CREATED
)
async def create_service(
        name: str,
        repo: RequestsRepo = Depends(get_repo)
):
    try:
        await repo.services.create(
            name=name
        )
    except Exception as e:
        await repo.session.rollback()
        logger.error(
            f"Error creating service. Details: {e}."
        )
        raise CannotAddDataToDatabase


@services_router.get(
    "",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_200_OK
)
async def get_services(
        repo: RequestsRepo = Depends(get_repo)
) -> List[SService]:
    services = await repo.services.get_all()
    return services


@services_router.delete(
    "/{name}",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_service(
        name: str,
        repo: RequestsRepo = Depends(get_repo)
):
    try:
        await repo.services.delete(name=name)
    except Exception as e:
        await repo.session.rollback()
        logger.error(
            f"Error deleting service. Details: {e}."
        )
        raise CannotDeleteDataFromDatabase
