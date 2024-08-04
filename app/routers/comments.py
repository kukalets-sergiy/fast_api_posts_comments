from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from app import crud
from app.dependencies import get_db
from app.profanity_checker import detect_toxicity
from app.routers.auth import access_security
from app.schemas.comment import CommentCreate, CommentResponse
from typing import List
from app.tasks import auto_reply_task

router = APIRouter()


@router.post("/", response_model=CommentResponse)
def create_comment(
        comment: CommentCreate,
        db: Session = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    is_blocked = detect_toxicity(comment.content)

    db_comment = crud.create_comment(
        db=db,
        comment=comment,
        user_id=credentials["id"],
        is_blocked=is_blocked
    )

    # Check if auto reply is enabled for this post
    post = crud.get_post(db, post_id=db_comment.post_id)
    if post.auto_reply_enabled:
        auto_reply_task.apply_async(
            args=(db_comment.post_id, db_comment.id),
            countdown=post.auto_reply_delay
        )
    # Receiving comments along with answers
    comment_with_replies = crud.get_comment_with_replies(db, comment_id=db_comment.id)
    return comment_with_replies


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.is_blocked:
        raise HTTPException(status_code=400, detail="Comment contains toxic content.")
    return db_comment


@router.get("/", response_model=List[CommentCreate])
def get_comments(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    comments = crud.get_comments(db, skip=skip, limit=limit)
    return comments


@router.put("/update/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.owner_id != credentials["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    if detect_toxicity(comment.content):
        raise HTTPException(status_code=400, detail="Comment contains toxic content.")

    updated_comment = crud.update_comment(db, comment=comment, comment_id=comment_id)
    return updated_comment


@router.delete("/delete/{comment_id}", response_model=CommentResponse)
def delete_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.owner_id != credentials["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    deleted_comment = crud.delete_comment(db, comment_id=comment_id)
    if deleted_comment:
        return JSONResponse(status_code=200, content={"detail": "Comment was deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Comment not found")
