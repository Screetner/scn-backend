from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta
from fastapi.encoders import jsonable_encoder

from database.connection import get_session
from database.mockData.faker import *
from database.schemas import OrganizationTable, RoleTable, UserTable, AssetTypeTable

router = APIRouter(
    prefix="/auth",
    tags=["faker"]
)


def custom_jsonable_encoder(obj):
    if isinstance(obj, WKTElement):
        return obj.desc
    if isinstance(obj.__class__, DeclarativeMeta):
        return {c.name: custom_jsonable_encoder(getattr(obj, c.name)) for c in obj.__table__.columns}
    return jsonable_encoder(obj)


@router.post("/insert-organization/")
async def insert_organization(db: AsyncSession = Depends(get_session)):
    mock_org_data = generate_mock_organization()
    new_org = OrganizationTable(**mock_org_data)

    mock_at_data = generate_mock_asserType()
    new_at = AssetTypeTable(**mock_at_data)

    async with db as session:
        session.add(new_org)
        await session.commit()
        await session.refresh(new_org)

        mock_role_data = generate_mock_role(new_org.OrganizationId)
        new_role = RoleTable(**mock_role_data)
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)

        mock_user_data = generate_mock_user(new_role.roleId)
        new_user = UserTable(**mock_user_data)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        session.add(new_at)
        await session.commit()
        await session.refresh(new_at)
