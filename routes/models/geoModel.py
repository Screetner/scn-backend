from typing import List
from pydantic import BaseModel


class LocationModel(BaseModel):
    lat: float
    long: float


class PostGeoModel(BaseModel):
    border: List[LocationModel]

