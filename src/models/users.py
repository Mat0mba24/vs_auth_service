from typing import List

from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db.base import Base, TableNameMixin


class User(Base, TableNameMixin):
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(nullable=True)
    hashed_password: Mapped[str]

    # Связь с ролями через таблицу user_roles
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="user_roles",  # Указываем промежуточную таблицу
        primaryjoin="User.user_id == UserRole.user_id",
        secondaryjoin="Role.role_id == UserRole.role_id",
        back_populates="users",
        lazy="selectin"
    )

    def __str__(self):
        return f"Пользователь #{self.user_id}."
