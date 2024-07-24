from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.dependencies import get_db
from app.schemas.post import PostCreate, PostResponse

router = APIRouter()


@router.post("/posts/", response_model=PostCreate)
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = 1):
    return crud.create_post(db=db, post=post, user_id=user_id)


@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.get("/", response_model=List[PostResponse])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts
