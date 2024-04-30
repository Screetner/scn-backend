import datetime

from sqlalchemy import Column, Integer, String, Double, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.connection import Base


class AssetTable(Base):
    __tablename__ = 'assets'

    assetId = Column(Integer, primary_key=True, index=True)
    latitude = Column(Double,)
    longitude = Column(Double,)
    recordedUser = Column(Integer, ForeignKey('users.uid'))
    assetTypeId = Column(Integer, ForeignKey('assetTypes.assetTypeId'))
    imageFileName = Column(String(255),)
    recordedAt = Column(DateTime, default=datetime.datetime.now)

    user = relationship("UserTable", back_populates="assets")
    assetType = relationship("AssetTypeTable", back_populates="assets")
