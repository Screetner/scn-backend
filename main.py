from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.connection import Base, engine
from routes import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
app.include_router(auth_router)
