from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from src.db.base import Base, TableNameMixin


class Service(Base, TableNameMixin):
    service_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)

    def __str__(self):
        return f"Сервис #{self.service_id}."
