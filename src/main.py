
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.api.endpoints import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await setup_database()
    ...
    yield
    ...


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


