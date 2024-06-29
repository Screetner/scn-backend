import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.connection import Base


class UserTable(Base):
    __tablename__ = 'users'

    UserId = Column(Integer, primary_key=True, index=True)
    roleId = Column(Integer, ForeignKey('roles.roleId'), nullable=True)
    username = Column(String(50), index=True)
    email = Column(String(100), index=True, unique=True)
    password = Column(String(100))
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    role = relationship("RoleTable", back_populates="users")
    assets = relationship("AssetTable", back_populates="user")
    videoSessions = relationship("VideoSessionTable", back_populates="user")
