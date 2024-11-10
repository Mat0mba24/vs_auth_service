from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from src.core.config import settings
from src.db.session import get_repo
from src.exceptions.custom_exceptions import TokenAbsentException, TokenExpiredException, IncorrectTokenFormatException, UserIsNotPresentException, NotEnoughPermissions
from src.models.users import User
from src.repositories.requests import RequestsRepo


def get_token(request: Request):
    token = request.cookies.get("auth_service_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(
        token: str = Depends(get_token),
        repo: RequestsRepo = Depends(get_repo)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await repo.users.get_one_or_none(user_id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def is_admin(
        current_user: User = Depends(get_current_user)
) -> None:
    if not any(role.name == "admin" for role in current_user.roles):
        raise NotEnoughPermissions
