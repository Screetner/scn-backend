import datetime

from sqlalchemy import Column, Integer, String, DateTime, Null
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from database.connection import Base


class OrganizationTable(Base):
    __tablename__ = 'organizations'

    OrganizationId = Column(Integer, primary_key=True, index=True)
    Name = Column(String(255), index=True, nullable=False)
    Border = Column(Geometry('POLYGON', srid=4326, spatial_index=None), nullable=True)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    role = relationship("RoleTable", back_populates="organization")
