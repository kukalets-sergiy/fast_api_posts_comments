from datetime import date
from app.schemas.user import OurBaseModel


class CommentsDailyBreakdown(OurBaseModel):
    date: date
    total_comments: int
    blocked_comments: int
