
from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from punq import Container, Scope

from src.config import get_settings, Settings

from src.db.core import AsyncSessionFactory

from src.infra.repositories import (
    RoleRepo,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=get_settings(), scope=Scope.singleton)

    settings = container.resolve(Settings)

    def init_async_session_factory() -> AsyncSessionFactory:
        engine = create_async_engine(settings.DATABASE_URL)
        async_session = async_sessionmaker(engine, expire_on_commit=False)

        return AsyncSessionFactory(async_session)

    container.register(AsyncSessionFactory, factory=init_async_session_factory, scope=Scope.singleton)

    #repositories
    container.register(RoleRepo, instance=RoleRepo(), scope=Scope.singleton)

    return container

