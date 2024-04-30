from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.connection import Base


class AssetTypeTable(Base):
    __tablename__ = 'assetTypes'

    assetTypeId = Column(Integer, primary_key=True, index=True)
    assetType = Column(String(255),)

    assets = relationship("AssetTable", back_populates="assetType")
