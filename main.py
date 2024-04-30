from fastapi import FastAPI
from routes import *
from database.connection import Base, engine

app = FastAPI()
app.include_router(root_router)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
