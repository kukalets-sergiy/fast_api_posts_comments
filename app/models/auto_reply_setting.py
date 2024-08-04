from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class AutoReplySetting(Base):
    __tablename__ = "auto_reply_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    delay_seconds = Column(Integer, default=2)
    is_enabled = Column(Boolean, default=True)

    user = relationship("User", back_populates="auto_reply_settings")
