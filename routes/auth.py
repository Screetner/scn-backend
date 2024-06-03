import os

import bcrypt
from authlib.jose import jwt
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_session
from database.schemas import UserTable
# logging
from logger import logger
from routes.models.authModel import SignInModel, SignUpModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signIn")
async def auth(sign_in_body: SignInModel, db: AsyncSession = Depends(get_session)):
    try:
        query = select(UserTable).filter((sign_in_body.username == UserTable.username))
        result = await db.execute(query)
        user = result.scalars().first()

        if not user or not bcrypt.checkpw(sign_in_body.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        header = {"alg": "HS256"}
        payload = {"username": user.username, "roleId": user.roleId}
        secret = os.getenv("JWT_SECRET")
        token = jwt.encode(header, payload, secret).decode("utf-8")
        return {"message": "Sign in successful", "token": token}
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signUp")
async def auth(sign_up_body: SignUpModel, db: AsyncSession = Depends(get_session)):
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(sign_up_body.password.encode('utf-8'), salt)
        new_user = UserTable(username=sign_up_body.username,
                             password=hashed.decode("utf-8"),
                             roleId=sign_up_body.roleId
                             )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"message": "User created successfully", "user": new_user}
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=400, detail="Error occurred while creating user")
