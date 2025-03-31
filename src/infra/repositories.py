
from abc import ABCMeta, abstractmethod

from sqlalchemy import select, update
from sqlalchemy.orm import load_only

from src.infra.schemas import AudiofileRespSchema, UserSchema

from src.db.models import (
    RoleOrm,
    AudioFileOrm,
    TokenOrm,
    UserOrm
)

from src.infra.schemas import AccessTokenSchemaDTO


class BaseSQLAlchemyRepo(metaclass=ABCMeta):

    @abstractmethod
    async def get(self, *args):
        raise NotImplemented

    @abstractmethod
    async def get_all(self, *args):
        raise NotImplemented

    @abstractmethod
    async def add(self, *args):
        raise NotImplemented

    @abstractmethod
    async def update(self, *args):
        raise NotImplemented


class UserRepo(BaseSQLAlchemyRepo):
    async def get(self, username: int, session):
        query = (
            select(UserOrm)
            .filter_by(username=username)
        )
        res = await session.scalars(query)
        return UserSchema.model_validate(res.one(), from_attributes=True)

    async def add(self):
        ...

    async def get_all(self):
        ...

    async def update(self):
        ...


class RoleRepo(BaseSQLAlchemyRepo):

    async def add(self, role: str, session):
        new_role = RoleOrm(role=role)
        session.add(new_role)
        return new_role

    async def get_all(self, session):
        q = select(RoleOrm)
        res = await session.execute(q)
        return res.scalars().all()

    async def get(self):
        ...

    async def update(self):
        ...


class AudioFileRepo(BaseSQLAlchemyRepo):
    async def add(self, name: str, path: str, user_id: int, session):
        new_file = AudioFileOrm(
            title=name,
            path=path,
            user_id=user_id
        )
        session.add(new_file)
        return new_file

    async def get(self, user_id: int, session):
        query = (
            select(AudioFileOrm)
            .options(load_only(AudioFileOrm.title, AudioFileOrm.path))
            .filter_by(user_id=user_id)
        )
        res = await session.scalars(query)
        res_orm = res.all()
        result = [AudiofileRespSchema.model_validate(row, from_attributes=True) for row in res_orm]
        return result

    async def get_all(self):
        ...

    async def update(self):
        ...


class TokenRepo(BaseSQLAlchemyRepo):
    async def update(self, data: AccessTokenSchemaDTO, user_id: int, session):
        stmt = (
            update(TokenOrm)
            .where(TokenOrm.user_id == user_id)
            .values(
                access_token=data.access_token,
                refresh_token=data.refresh_token,
                expires_in=str(data.expires_in)
            )
        )
        await session.execute(stmt)

    async def get(self):
        ...

    async def get_all(self):
        ...

    async def add(self):
        ...
