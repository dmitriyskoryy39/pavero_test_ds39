
from contextlib import asynccontextmanager

from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


Base: DeclarativeMeta = declarative_base()

#
# class Base(DeclarativeBase):
#     pass


class AsyncSessionFactory:

    def __init__(self, async_session: async_sessionmaker):
        self.async_session = async_session

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session
