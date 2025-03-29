
from abc import ABCMeta, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.schemas import RoleAddSchema
from src.db.models import RoleOrm


class BaseSQLAlchemyRepo(metaclass=ABCMeta):

    @abstractmethod
    async def get(self, session):
        raise NotImplemented

    @abstractmethod
    async def get_all(self, session):
        raise NotImplemented

    @abstractmethod
    async def add(self, role: str, session):
        raise NotImplemented


class RoleRepo(BaseSQLAlchemyRepo):

    async def add(self, role: str, session):
        new_role = RoleOrm(role=role)
        session.add(new_role)
        await session.commit()
        return {"ok": True}

    async def get_all(self, session):
        q = select(RoleOrm)
        res = await session.execute(q)
        return res.scalars().all()

    async def get(self):
        ...
