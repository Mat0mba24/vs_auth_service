from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.service_id", ondelete="CASCADE"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.role_id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint(
            "user_id", "service_id",
            name="unique_user_service_role"
        ),
    )
