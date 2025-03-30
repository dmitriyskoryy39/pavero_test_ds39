
from abc import ABCMeta, abstractmethod

from sqlalchemy import select

from src.infra.schemas import RoleAddSchema

from src.db.models import (
    RoleOrm,
    AudioFileOrm
)


class BaseSQLAlchemyRepo(metaclass=ABCMeta):

    @abstractmethod
    async def get_by_id(self, *args):
        raise NotImplemented

    @abstractmethod
    async def get_all(self, *args):
        raise NotImplemented

    @abstractmethod
    async def add(self, *args):
        raise NotImplemented


class RoleRepo(BaseSQLAlchemyRepo):

    async def add(self, role: str, session):
        new_role = RoleOrm(role=role)
        session.add(new_role)
        return new_role

    async def get_all(self, session):
        q = select(RoleOrm)
        res = await session.execute(q)
        return res.scalars().all()

    async def get_by_id(self):
        ...


class AudioFileRepo(BaseSQLAlchemyRepo):
    async def add(self, title: str, path: str, user_id: int, session):
        new_file = AudioFileOrm(
            title=title,
            path=path,
            user_id=user_id
        )
        session.add(new_file)
        return new_file

    async def get_all(self, session):
        ...

    async def get_by_id(self, user_id: int, session):
        q = select(
            AudioFileOrm.title,
            AudioFileOrm.path
        ).filter_by(user_id=user_id)
        res = await session.execute(q)
        return res.scalars().all()
