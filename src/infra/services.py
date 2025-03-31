
from abc import ABCMeta

from pathlib import Path

from fastapi import UploadFile

from aiofile import async_open

from src.infra.repositories import BaseSQLAlchemyRepo

from src.db.core import AsyncSessionFactory

from src.infra.schemas import AccessTokenSchemaDTO, UserLoginDTO


class BaseService(metaclass=ABCMeta):
    def __init__(self, repo: BaseSQLAlchemyRepo | dict, session_factory: AsyncSessionFactory):
        self.repo = repo
        self.session_factory = session_factory

    def __call__(self):
        return self


class FileService(BaseService):

    @property
    async def get_path(self):
        base_dir = Path().cwd()
        return base_dir / 'storage'

    async def upload(
        self,
        uploaded_file: UploadFile,
        name: str,
        user: UserLoginDTO
    ):
        try:
            file = uploaded_file.file
            filename = await self.get_path / uploaded_file.filename
            async with async_open(filename, 'wb') as f:
                await f.write(file.read())

            async with self.session_factory.get_session() as session:
                repo_user = self.repo.get('UserRepo')
                user_id = await repo_user.get(user.login, session)
                repo_audio = self.repo.get('AudioFileRepo')
                res = await repo_audio.add(name=name, path=str(filename), user_id=user_id.id, session=session)
                await session.commit()
                return res
        except Exception as e:
            print(e)

    async def get(self, user: UserLoginDTO):
        try:
            async with self.session_factory.get_session() as session:
                repo_user = self.repo.get('UserRepo')
                repo_audio = self.repo.get('AudioFileRepo')

                user = await repo_user.get(user.login, session)
                if user:
                    res = await repo_audio.get(user.id, session)
                    return res
                return None
        except Exception as e:
            print(e)


class LoginService(BaseService):
    async def login(self, login: str, token_data: AccessTokenSchemaDTO):
        try:
            async with self.session_factory.get_session() as session:
                repo_user = self.repo.get('UserRepo')
                repo_token = self.repo.get('TokenRepo')

                user = await repo_user.get(login, session)
                if user:
                    await repo_token.update(token_data, user.id, session)
                    await session.commit()
                    return
                user = await repo_user.add(login, session)
                await repo_token.add(token_data, user.id, session)
                await session.commit()
        except Exception as e:
            print(e)

