
from functools import lru_cache

from punq import Container, Scope

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine


from src.config import get_settings, Settings


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Settings, instance=get_settings(), scope=Scope.singleton)

    settings = container.resolve(Settings)
    container.register(AsyncEngine, instance=create_async_engine(settings.DATABASE_URL), scope=Scope.singleton)
    engine = container.resolve(AsyncEngine)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    class Session:
        @staticmethod
        async def get_session() -> AsyncSession:
            async with async_session() as session:
                yield session

    container.register(AsyncSession, instance=Session.get_session(), scope=Scope.singleton)

    return container

