
from abc import ABCMeta

from pathlib import Path

from fastapi import UploadFile

from aiofile import async_open

from src.infra.repositories import BaseSQLAlchemyRepo

from src.db.core import AsyncSessionFactory

from src.infra.schemas import AccessTokenSchema


class BaseService(metaclass=ABCMeta):
    def __init__(self, repo: BaseSQLAlchemyRepo | dict, session_factory: AsyncSessionFactory):
        self.repo = repo
        self.session_factory = session_factory

    def __call__(self):
        return self


class RoleService(BaseService):
    async def add(self, role: str):
        try:
            async with self.session_factory.get_session() as session:
                res = await self.repo.add(role, session)
                await session.commit()
                return res
        except Exception as e:
            print(e)

    async def get_all(self):
        try:
            async with self.session_factory.get_session() as session:
                res = await self.repo.get_all(session)
                return res
        except Exception as e:
            print(e)


class FileService(BaseService):

    @property
    async def get_path(self):
        base_dir = Path().cwd()
        return base_dir / 'storage'

    async def upload(
        self,
        uploaded_file: UploadFile,
        name: str,
        user_id: int
    ):
        try:
            file = uploaded_file.file
            filename = await self.get_path / uploaded_file.filename
            async with async_open(filename, 'wb') as f:
                await f.write(file.read())

            async with self.session_factory.get_session() as session:
                res = await self.repo.add(name, str(filename), user_id, session)
                await session.commit()
                return res
        except Exception as e:
            print(e)

    async def get(self, user_id: int):
        try:
            async with self.session_factory.get_session() as session:
                res = await self.repo.get(user_id, session)
                return res
        except Exception as e:
            print(e)


class LoginService(BaseService):
    async def login(self, login: str, token_data: AccessTokenSchema):
        try:
            async with self.session_factory.get_session() as session:
                repo_user = self.repo.get('UserRepo')
                user = await repo_user.get(login, session)
                if not user:
                    raise Exception
                repo_token = self.repo.get('TokenRepo')
                await repo_token.update(token_data, user.id, session)
                await session.commit()
        except Exception as e:
            print(e)
