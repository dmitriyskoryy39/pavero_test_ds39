
from contextlib import asynccontextmanager

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


class Base(DeclarativeBase):
    pass


class AsyncSessionFactory:

    def __init__(self, async_session: async_sessionmaker):
        self.async_session = async_session

    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        async with self.async_session() as session:
            yield session
