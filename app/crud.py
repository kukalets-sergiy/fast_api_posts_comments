from collections import defaultdict
from datetime import date
from sqlalchemy.orm import Session
from app.models.auto_reply_setting import AutoReplySetting
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate
from app.schemas.post import PostCreate, PostResponse
from app.schemas.user import UserCreate


# User CRUD operations

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, user_id: int) -> PostResponse:
    db_post = Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        owner_id=db_post.owner_id
    )


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()


def update_post(db: Session, post: PostCreate, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post


def create_comment(db: Session, comment: CommentCreate, user_id: int, is_blocked: bool):
    db_comment = Comment(**comment.dict(), owner_id=user_id, is_blocked=is_blocked)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Comment).filter(Comment.is_blocked == False).offset(skip).limit(limit).all()


def update_comment(db: Session, comment: CommentCreate, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db_comment.content = comment.content
        db.commit()
        db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment


def check_password(self, password: str) -> bool:
    return self.hashed_password == password


def get_comments_daily_breakdown(db: Session, date_from: date, date_to: date):
    comments = db.query(Comment).filter(Comment.created_at >= date_from, Comment.created_at <= date_to).all()
    analytics = defaultdict(lambda: {'total_comments': 0, 'blocked_comments': 0})

    for comment in comments:
        comment_date = comment.created_at.date()
        analytics[comment_date]['total_comments'] += 1
        if comment.is_blocked:
            analytics[comment_date]['blocked_comments'] += 1

    return [{'date': date, **data} for date, data in analytics.items()]


def get_auto_reply_setting(db: Session, user_id: int):
    return db.query(AutoReplySetting).filter(AutoReplySetting.user_id == user_id).first()

def create_or_update_auto_reply_setting(db: Session, user_id: int, delay_seconds: int, is_enabled: bool):
    setting = db.query(AutoReplySetting).filter(AutoReplySetting.user_id == user_id).first()
    if setting:
        setting.delay_seconds = delay_seconds
        setting.is_enabled = is_enabled
    else:
        setting = AutoReplySetting(user_id=user_id, delay_seconds=delay_seconds, is_enabled=is_enabled)
        db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting
