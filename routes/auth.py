import os

import bcrypt
from authlib.jose import jwt
from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from fastapi.responses import JSONResponse

from database.connection import get_session
from database.schemas import UserTable, OrganizationTable, RoleTable
# logging
from logger import logger
from routes.models.authModel import SignInModel, SignUpModel, JwtPayload

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signIn")
async def auth(sign_in_body: SignInModel, response: Response, db: AsyncSession = Depends(get_session)):
    try:
        query = select(UserTable).filter((sign_in_body.username == UserTable.username))
        result = await db.execute(query)
        user = result.scalars().first()

        if not user or not bcrypt.checkpw(sign_in_body.password.encode('utf-8'), user.password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        query = (
            select(RoleTable)
            .join(UserTable, RoleTable.roleId == UserTable.roleId)
            .join(OrganizationTable, (RoleTable.OrganizationId == OrganizationTable.OrganizationId))
            .options(
                joinedload(RoleTable.organization),
                joinedload(RoleTable.users)
            )
            .where((sign_in_body.username == UserTable.username))
        )

        result = (await db.execute(query)).scalars().first()

        header = {"alg": "HS256"}
        payload = JwtPayload(userId=user.UserId, roleId=user.roleId, organizationId=result.OrganizationId)
        print(payload.model_dump())
        secret = os.getenv("JWT_ACCESS_SECRET")
        token = jwt.encode(header, payload.model_dump(), secret).decode("utf-8")
        response = {
            "token": token,
            "user": {
                "username": user.username,
                "roleId": user.roleId,
                "roleName": result.roleName,
                "email": user.email,
                "organization_name": result.organization.Name,
            }
        }
        return JSONResponse(content=response, status_code=200)
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
