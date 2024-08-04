from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.user import User


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey("posts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_blocked = Column(Boolean, default=False)
    parent_comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)

    post = relationship("Post", back_populates="comments")
    owner = relationship("User", back_populates="comments")
    parent_comment = relationship("Comment", remote_side=[id], backref="replies")
