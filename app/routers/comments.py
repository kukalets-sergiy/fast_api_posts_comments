from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app import crud
from app.dependencies import get_db
from app.profanity_checker import detect_toxicity
from app.routers.auth import access_security
from app.schemas.comment import CommentResponse, CommentCreate

router = APIRouter()


@router.post("/", response_model=CommentCreate)
async def create_comment(
        comment: CommentCreate,
        db: AsyncSession = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    # Check for toxic content in the comment
    if detect_toxicity(comment.content):
        raise HTTPException(status_code=400, detail="Comment contains toxic content.")

    user_id = credentials["id"]
    # Create and return the comment
    return await crud.create_comment(db=db, comment=comment, user_id=user_id)


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(
        comment_id: int,
        db: AsyncSession = Depends(get_db)
):
    # Fetch the comment from the database
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    return db_comment


@router.get("/", response_model=List[CommentResponse])
async def get_comments(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    comments = await crud.get_comments(db, skip=skip, limit=limit)
    return comments


@router.put("/update/{comment_id}", response_model=CommentResponse)
async def update_comment(
        comment_id: int,
        comment: CommentCreate,
        db: AsyncSession = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    # Getting a comment from the database
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Checking access rights
    if db_comment.owner_id != credentials["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    # Checking for toxic content
    if detect_toxicity(comment.content):
        raise HTTPException(status_code=400, detail="Comment contains toxic content.")

    # Comment update
    updated_comment = await crud.update_comment(db, comment=comment, comment_id=comment_id)
    return updated_comment


@router.delete("/delete/{comment_id}", response_model=CommentResponse)
async def delete_comment(
        comment_id: int,
        db: AsyncSession = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    db_comment = await crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.owner_id != credentials["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    deleted_comment = await crud.delete_comment(db, comment_id=comment_id)
    if deleted_comment:
        return JSONResponse(status_code=200, content={"detail": "Comment was deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Comment not found")