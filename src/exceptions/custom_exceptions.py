from fastapi import HTTPException, status


class AuthServiceBaseException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(AuthServiceBaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class UserNotExistsException(AuthServiceBaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователя не существует"


class UserRoleAlreadyExistsException(AuthServiceBaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Роль пользователя уже существует"


class IncorrectUsernameOrPasswordException(AuthServiceBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"


class TokenExpiredException(AuthServiceBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(AuthServiceBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(AuthServiceBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(AuthServiceBaseException):
    status_code = status.HTTP_401_UNAUTHORIZED


class CannotAddDataToDatabase(AuthServiceBaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"


class CannotDeleteDataFromDatabase(AuthServiceBaseException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось удалить запись"


class NotEnoughPermissions(AuthServiceBaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "У пользователя недостаточно прав"
