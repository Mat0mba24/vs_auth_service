from src.api.auth import auth_router
from src.api.roles import roles_router
from src.api.services import services_router
from src.api.users import users_router

all_routers = (
    auth_router,
    users_router,
    services_router,
    roles_router
)
