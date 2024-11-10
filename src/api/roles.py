from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.api.dependencies import is_admin
from src.core.logger import logger
from src.db.session import get_repo
from src.exceptions.custom_exceptions import CannotAddDataToDatabase, CannotDeleteDataFromDatabase
from src.repositories.requests import RequestsRepo
from src.schemas.roles import SRole

roles_router = APIRouter(
    prefix="/roles",
    tags=["Роли"]
)


@roles_router.post(
    "",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_201_CREATED
)
async def create_role(
        name: str,
        repo: RequestsRepo = Depends(get_repo)
):
    try:
        await repo.roles.create(
            name=name
        )
    except Exception as e:
        await repo.session.rollback()
        logger.error(
            f"Error creating role. Details: {e}."
        )
        raise CannotAddDataToDatabase


@roles_router.get(
    "",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_200_OK
)
async def get_roles(
        repo: RequestsRepo = Depends(get_repo)
) -> List[SRole]:
    roles = await repo.roles.get_all()
    return roles


@roles_router.delete(
    "/{name}",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_role(
        name: str,
        repo: RequestsRepo = Depends(get_repo)
):
    try:
        await repo.roles.delete(name=name)
    except Exception as e:
        await repo.session.rollback()
        logger.error(
            f"Error deleting role. Details: {e}."
        )
        raise CannotDeleteDataFromDatabase
