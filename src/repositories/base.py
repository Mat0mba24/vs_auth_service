from typing import List, Dict

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    model = None

    def __init__(self, session):
        self.session: AsyncSession = session

    async def create(
            self,
            **params
    ) -> None:
        insert_stmt = (
            insert(
                self.model
            )
            .values(
                **params
            )
            .on_conflict_do_nothing()
        )
        await self.session.execute(insert_stmt)
        await self.session.commit()

    async def get_all(
            self,
            limit: int = 10,
            offset: int = 0
    ) -> List[Dict]:
        select_stmt = (
            select(
                self.model.__table__.columns
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(select_stmt)
        return result.mappings().all()

    async def delete(
            self,
            **filter_by
    ) -> None:
        delete_stmt = (
            delete(
                self.model
            )
            .filter_by(
                **filter_by
            )
        )
        await self.session.execute(delete_stmt)
        await self.session.commit()

    async def get_one_or_none(
            self,
            **filter_by
    ):
        select_stmt = (
            select(
                self.model
            )
            .filter_by(
                **filter_by
            )
        )
        result = await self.session.scalar(select_stmt)
        return result
