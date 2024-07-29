from datetime import date
from fastapi import Depends, HTTPException, APIRouter
from typing import List
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.schemas.analytics import CommentsDailyBreakdown


router = APIRouter()


@router.get("/comments-daily-breakdown",
            response_model=List[CommentsDailyBreakdown],
            summary="Get daily breakdown of comments",
            description="Returns analytics on the number of comments created for posts over a specified period. "
                        "The date format should be YYYY-MM-DD. Example:"
                        "/api/comments-daily-breakdown?date_from=2024-07-23&date_to=2024-08-01")
def comments_daily_breakdown(
    date_from: date,
    date_to: date,
    db: Session = Depends(get_db)
):
    if date_from > date_to:
        raise HTTPException(status_code=400, detail="date_from must be earlier than date_to")

    analytics = crud.get_comments_daily_breakdown(db, date_from, date_to)
    return analytics
