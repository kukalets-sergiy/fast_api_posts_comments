import datetime
from app.schemas.user import OurBaseModel


class CommentCreate(OurBaseModel):
    content: str
    post_id: int


class CommentResponse(OurBaseModel):
    id: int
    content: str
    post_id: int
    owner_id: int
    created_at: datetime.date


