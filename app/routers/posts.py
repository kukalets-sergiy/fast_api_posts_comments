from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app import crud
from app.dependencies import get_db
from app.profanity_checker import detect_toxicity
from app.routers.auth import access_security
from app.schemas.post import PostCreate, PostResponse

router = APIRouter()


@router.post("/", response_model=PostCreate)
def create_post(
        post: PostCreate,
        db: Session = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):

    if detect_toxicity(post.title) or detect_toxicity(post.content):
        raise HTTPException(status_code=400, detail="Post contains toxic content.")

    user_id = credentials["id"]
    return crud.create_post(db=db, post=post, user_id=user_id)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.get("/", response_model=List[PostResponse])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.put("/update/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != credentials["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    if detect_toxicity(post.title) or detect_toxicity(post.content):
        raise HTTPException(status_code=400, detail="Post contains toxic content.")

    updated_post = crud.update_post(db, post=post, post_id=post_id)
    return updated_post


@router.delete("/delete/{post_id}", response_model=PostResponse)
def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != credentials["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    deleted_post = crud.delete_post(db, post_id=post_id)
    if deleted_post:
        return JSONResponse(status_code=200, content={"detail": "Post was deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Post not found")
