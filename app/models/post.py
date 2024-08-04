from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    auto_reply_enabled = Column(Boolean, default=False)
    auto_reply_delay = Column(Integer, default=2)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
