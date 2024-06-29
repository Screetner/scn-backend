import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from database.connection import Base


class AssetTable(Base):
    __tablename__ = 'assets'

    assetId = Column(Integer, primary_key=True, index=True)
    geoCoordinate = Column(Geometry('POINT'))
    assetTypeId = Column(Integer, ForeignKey('assetTypes.assetTypeId'), index=True)
    imageFileLink = Column(String(255),)
    recordedUser = Column(Integer, ForeignKey('users.UserId'))
    recordedAt = Column(DateTime)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship("UserTable", back_populates="assets")
    assetType = relationship("AssetTypeTable", back_populates="assets")
