from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.connection import Base


class UserTable(Base):
    __tablename__ = 'users'

    uid = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True,)
    roleId = Column(Integer, ForeignKey('roles.roleId'))
    password = Column(String(255),)

    role = relationship("RoleTable", back_populates="users")
    assets = relationship("AssetTable", back_populates="user")
