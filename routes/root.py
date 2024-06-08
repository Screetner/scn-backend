from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from database.schemas import TestTable

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World! This is the Screetner project that made by SlowAPI."}