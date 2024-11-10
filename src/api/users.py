from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.api.dependencies import is_admin
from src.core.auth import get_password_hash
from src.core.logger import logger
from src.db.session import get_repo
from src.exceptions.custom_exceptions import (
    UserAlreadyExistsException,
    UserNotExistsException,
    CannotAddDataToDatabase,
    CannotDeleteDataFromDatabase,
    UserRoleAlreadyExistsException
)
from src.repositories.requests import RequestsRepo
from src.schemas.users import SUser, SCreateUser

users_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@users_router.get(
    "",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_200_OK
)
async def get_users(
        limit: int = 10,
        offset: int = 0,
        repo: RequestsRepo = Depends(get_repo)
) -> List[SUser]:
    users = await repo.users.get_all(
        limit=limit,
        offset=offset
    )
    return users


@users_router.post(
    "",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        create_user_data: SCreateUser,
        repo: RequestsRepo = Depends(get_repo)
):
    existing_user = await repo.users.get_one_or_none(username=create_user_data.username)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(create_user_data.password)

    try:
        await repo.users.create(
            username=create_user_data.username,
            hashed_password=hashed_password
        )
    except Exception as e:
        await repo.session.rollback()
        logger.error(
            f"Error creating user. Details: {e}."
        )
        raise CannotAddDataToDatabase


@users_router.post(
    "/access",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_201_CREATED
)
async def add_access(
        username: str,
        role: str,
        service: str,
        repo: RequestsRepo = Depends(get_repo)
):
    existing_user = await repo.users.get_one_or_none(username=username)
    if not existing_user:
        raise UserNotExistsException

    user_role_is_exists = await repo.user_roles.is_exists(
        username=username,
        role=role,
        service=service
    )
    if user_role_is_exists:
        raise UserRoleAlreadyExistsException

    try:
        await repo.user_roles.create(
            username=username,
            role=role,
            service=service
        )
    except Exception as e:
        await repo.session.rollback()
        logger.error(
            f"Error adding access to user. Details: {e}."
        )
        raise CannotAddDataToDatabase


@users_router.delete(
    "/{username}",
    dependencies=[Depends(is_admin)],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
        username: str,
        repo: RequestsRepo = Depends(get_repo)
):
    existing_user = await repo.users.get_one_or_none(username=username)
    if not existing_user:
        raise UserNotExistsException

    try:
        await repo.users.delete(username=username)
    except Exception as e:
        await repo.session.rollback()
        logger.error(
            f"Error deleting user. Details: {e}."
        )
        raise CannotDeleteDataFromDatabase
