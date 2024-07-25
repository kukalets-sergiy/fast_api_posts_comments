from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from app import crud
from app.dependencies import get_db
from app.routers.auth import access_security
from app.schemas.comment import CommentCreate, CommentResponse

router = APIRouter()


@router.post("/comments/", response_model=CommentCreate)
def create_comment(
        comment: CommentCreate,
        db: Session = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["id"]
    return crud.create_comment(db=db, comment=comment, user_id=user_id)


@router.get("/comments/{comment_id}", response_model=CommentResponse)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.get("/", response_model=List[CommentResponse])
def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, skip=skip, limit=limit)
    return comments
