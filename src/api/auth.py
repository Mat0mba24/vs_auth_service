from fastapi import APIRouter, Depends
from starlette.responses import Response

from src.db.session import get_repo
from src.repositories.requests import RequestsRepo
from src.schemas.auth import SUserAuth
from src.core.auth import authenticate_user, create_access_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/login")
async def login_user(
        response: Response,
        user_auth_data: SUserAuth,
        repo: RequestsRepo = Depends(get_repo)
):
    user = await authenticate_user(
        username=user_auth_data.username,
        password=user_auth_data.password,
        repo=repo
    )
    access_token = create_access_token({"sub": str(user.user_id)})
    response.set_cookie("auth_service_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("auth_service_access_token")
