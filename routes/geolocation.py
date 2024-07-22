from fastapi import APIRouter, Request
from fastapi.params import Depends
from geoalchemy2 import WKTElement
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_session
from database.schemas import OrganizationTable
from functions.geolocation.geo import format_polygon
from routes.models.geoModel import PostGeoModel

router = APIRouter(
    prefix="/geolocation",
    tags=["geo"]
)


@router.post("/post")
async def post_geo(geo_model: PostGeoModel, request: Request, db: AsyncSession = Depends(get_session)):
    token_payload = request.state.token_payload
    location = format_polygon(geo_model)

    try:
        polygon_wkt = WKTElement(location, srid=4326)
    except Exception as e:
        return {"message": f"Error creating WKTElement: {str(e)}"}, 400

    try:
        organization_id = token_payload['organizationId']
        async with db as session:
            async with session.begin():
                org = await session.get(OrganizationTable, organization_id)
                if org:
                    org.Border = polygon_wkt
                    session.add(org)
                    await session.commit()
                    return {"message": f"Organization {organization_id} geometry updated successfully"}
                else:
                    return {"message": f"Organization with id {organization_id} not found"}, 404
    except Exception as e:
        print(e)
        return {"message": f"Error occurred: {str(e)}"}, 500
