from sqlalchemy import Column, Integer, String

from database.connection import Base


class TestTable(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True,)
    age = Column(Integer)
