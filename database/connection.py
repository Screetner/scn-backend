import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

load_dotenv()

DATABASE_URL = f'mysql+aiomysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session = async_sessionmaker(engine, expire_on_commit=False)
engine = sessionmaker(DATABASE_URL, expire_on_commit=False)
session = Session(engine)


class Base(DeclarativeBase):
    pass


# async def get_session():
#     db = async_session()
#     try:
#         yield db
#     finally:
#         await db.close()

def get_session():
    db = session
    try:
        yield db
    finally:
        db.close()
