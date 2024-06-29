import datetime
from enum import Enum

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship

from database.connection import Base


class VideoSessionStateEnum(Enum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    CAN_DELETE = "canDelete"


class VideoSessionTable(Base):
    __tablename__ = 'videoSessions'

    VideoSessionId = Column(Integer, primary_key=True)
    uploadUserId = Column(Integer, ForeignKey('users.UserId'))
    uploadProgress = Column(Float)
    videoLink = Column(String(255))
    state = Column(SQLAlchemyEnum(VideoSessionStateEnum), nullable=False)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    user = relationship("UserTable", back_populates="videoSessions")
