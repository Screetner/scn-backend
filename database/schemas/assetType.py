import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database.connection import Base


class AssetTypeTable(Base):
    __tablename__ = 'assetTypes'

    assetTypeId = Column(Integer, primary_key=True, index=True)
    assetType = Column(String(255),)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    assets = relationship("AssetTable", back_populates="assetType")
