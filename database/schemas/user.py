from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class UserTable(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True,)
    roleId = Column(Integer, ForeignKey('roles.roleId'), nullable=True)
    password = Column(String(100),)

    role = relationship("RoleTable", back_populates="users")
    assets = relationship("AssetTable", back_populates="user")
