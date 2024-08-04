import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.user import OurBaseModel


class CommentCreate(OurBaseModel):
    content: str
    post_id: int


class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    owner_id: int
    parent_comment_id: Optional[int] = None
    is_blocked: bool
    created_at: datetime.date
    replies: List["CommentResponse"] = []

    class Config:
        orm_mode = True




