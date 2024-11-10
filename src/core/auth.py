from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings
from src.exceptions.custom_exceptions import IncorrectUsernameOrPasswordException
from src.repositories.requests import RequestsRepo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
    )
    return encoded_jwt


async def authenticate_user(
        username: str,
        password: str,
        repo: RequestsRepo
):
    user = await repo.users.get_one_or_none(username=username)
    if not (user and verify_password(password, user.hashed_password)):
        raise IncorrectUsernameOrPasswordException
    return user
