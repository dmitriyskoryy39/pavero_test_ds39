
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.api.endpoints import router as api_router
from src.infra.oauth.yandex import router as router_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await setup_database()
    ...
    yield
    ...


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
app.include_router(router_auth)


