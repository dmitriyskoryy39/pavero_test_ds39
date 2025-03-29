
from typing import Annotated
from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.container import Container, init_container
from src.infra.repositories import RoleRepo

from src.db.core import AsyncSessionFactory


container: Container = init_container()
async_session_factory = container.resolve(AsyncSessionFactory)

router = APIRouter()


Session = Annotated[AsyncSession, Depends(async_session_factory.get_session)]
container: Container = init_container()


@router.get('/get_all')
async def get_all(session: Session):
    repo = container.resolve(RoleRepo)

    # session.add(new_role)
    roles = await repo.get_all(session)
    return roles
