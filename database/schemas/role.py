import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship

from database.connection import Base


class RoleTable(Base):
    __tablename__ = 'roles'

    roleId = Column(Integer, primary_key=True, index=True)
    OrganizationId = Column(Integer, ForeignKey('organizations.OrganizationId'), index=True)
    roleName = Column(String(255))
    abilityScope = Column(JSON)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    organization = relationship("OrganizationTable", back_populates="role")
    users = relationship("UserTable", back_populates="role")
