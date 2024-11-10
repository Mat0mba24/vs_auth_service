from typing import List

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.db.base import Base, TableNameMixin


class Role(Base, TableNameMixin):
    role_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    # Связь с пользователями через таблицу user_roles
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_roles",
        primaryjoin="Role.role_id == UserRole.role_id",
        secondaryjoin="User.user_id == UserRole.user_id",
        back_populates="roles",
        lazy="selectin"
    )

    def __str__(self):
        return f"Роль #{self.role_id}."
