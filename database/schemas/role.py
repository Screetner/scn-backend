from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.connection import Base


class RoleTable(Base):
    __tablename__ = 'roles'

    roleId = Column(Integer, primary_key=True, index=True)
    roleName = Column(String(255), index=True,)
    roleCode = Column(String(255),)

    users = relationship("UserTable", back_populates="role")
