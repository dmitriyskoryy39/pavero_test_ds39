
from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from punq import Container, Scope

from src.config import get_settings, Settings

from src.db.core import AsyncSessionFactory

from src.infra.services import (
    RoleService,
    FileService,
    LoginService
)

from src.infra.repositories import (
    RoleRepo,
    AudioFileRepo,
    TokenRepo,
    UserRepo
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=get_settings(), scope=Scope.singleton)

    settings = container.resolve(Settings)

    def init_async_session_factory() -> AsyncSessionFactory:
        engine = create_async_engine(settings.POSTGRES_DSN)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        return AsyncSessionFactory(async_session)

    def init_role_service() -> RoleService:
        return RoleService(RoleRepo(), init_async_session_factory())

    def init_file_service() -> FileService:
        repos = {
            'AudioFileRepo': AudioFileRepo(),
            'UserRepo': UserRepo()
        }
        return FileService(repos, init_async_session_factory())

    def init_login_service() -> LoginService:
        repos = {
            'UserRepo': UserRepo(),
            'TokenRepo': TokenRepo()
        }
        return LoginService(repos, init_async_session_factory())


    #services
    container.register(
        RoleService,
        factory=init_role_service,
        scope=Scope.singleton
    )
    container.register(
        FileService,
        factory=init_file_service,
        scope=Scope.singleton
    )
    container.register(
        LoginService,
        factory=init_login_service,
        scope=Scope.singleton
    )

    return container

