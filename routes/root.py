from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_session
from database.schemas import test

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World! AUjung"}


@router.get("/test")
def testQuery(db: Session = Depends(get_session)):
    results = db.query(test).all()
    return {"user": results}