from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.connection import get_session
from database.schemas import test, TestTable

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World! AUjung"}


@router.get("/test")
async def testQuery(db: AsyncSession = Depends(get_session)):
    results = await db.execute(select(TestTable))
    users = results.scalars().all()
    return {"user": users}
