
from src.infra.repositories import BaseSQLAlchemyRepo

from src.db.core import AsyncSessionFactory


class RoleService:

    def __init__(self, repo: BaseSQLAlchemyRepo, session_factory: AsyncSessionFactory):
        self.repo = repo
        self.session_factory = session_factory

    def __call__(self):
        return self

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
