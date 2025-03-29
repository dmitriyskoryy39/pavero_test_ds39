
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.api.endpoints import router as api_router


# from sqlalchemy.ext.asyncio import AsyncEngine
#

# async def setup_database():
#     container: Container = init_container()
#     engine = container.resolve(AsyncEngine)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await setup_database()
    ...
    yield
    ...


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


