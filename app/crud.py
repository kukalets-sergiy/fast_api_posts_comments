from sqlalchemy.orm import Session
from app.models import user as user_model, post as post_model, comment as comment_model, auto_reply_setting as auto_reply_setting_model
from app.models.user import User
from app.schemas.auto_reply_setting import AutoReplySettingCreate
from app.schemas.comment import CommentCreate
from app.schemas.post import PostCreate
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
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(user_model.User).offset(skip).limit(limit).all()


# Post CRUD operations
def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = post_model.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def get_post(db: Session, post_id: int):
    return db.query(post_model.Post).filter(post_model.Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(post_model.Post).offset(skip).limit(limit).all()


# Comment CRUD operations
def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = comment_model.Comment(**comment.dict(), owner_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int):
    return db.query(comment_model.Comment).filter(comment_model.Comment.id == comment_id).first()


def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(comment_model.Comment).offset(skip).limit(limit).all()


# AutoReplySetting CRUD operations
def create_auto_reply_setting(db: Session, auto_reply_setting: AutoReplySettingCreate, user_id: int):
    db_auto_reply_setting = auto_reply_setting_model.AutoReplySetting(**auto_reply_setting.dict(), user_id=user_id)
    db.add(db_auto_reply_setting)
    db.commit()
    db.refresh(db_auto_reply_setting)
    return db_auto_reply_setting


def get_auto_reply_setting(db: Session, auto_reply_setting_id: int):
    return db.query(auto_reply_setting_model.AutoReplySetting).filter(
        auto_reply_setting_model.AutoReplySetting.id == auto_reply_setting_id).first()
