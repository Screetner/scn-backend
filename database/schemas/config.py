from sqlalchemy import Column, Integer, String

from database.connection import Base


class ConfigTable(Base):
    __tablename__ = 'configs'

    configId = Column(Integer, primary_key=True, index=True)
    config = Column(String(255),)
