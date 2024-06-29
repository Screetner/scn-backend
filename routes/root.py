from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"message": "Hello World! This is the Screetner project that made by SlowAPI."}