from collections import defaultdict
from datetime import date
from app.models.auto_reply_setting import AutoReplySetting
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.auto_reply_setting import AutoReplySettingCreate
from app.schemas.comment import CommentCreate
from app.schemas.post import PostCreate, PostResponse
from app.schemas.user import UserCreate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user(db: AsyncSession, user_id: int):
    stmt = select(User).filter(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).filter(User.email == email)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(User).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_post(db: AsyncSession, post: PostCreate, user_id: int) -> PostResponse:
    db_post = Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        owner_id=db_post.owner_id
    )


async def get_post(db: AsyncSession, post_id: int):
    stmt = select(Post).filter(Post.id == post_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Post).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_post(db: AsyncSession, post: PostCreate, post_id: int):
    stmt = select(Post).filter(Post.id == post_id)
    result = await db.execute(stmt)
    db_post = result.scalars().first()
    if db_post:
        db_post.title = post.title
        db_post.content = post.content
        await db.commit()
        await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, post_id: int):
    stmt = select(Post).filter(Post.id == post_id)
    result = await db.execute(stmt)
    db_post = result.scalars().first()
    if db_post:
        await db.delete(db_post)
        await db.commit()
    return db_post


async def create_comment(db: AsyncSession, comment: CommentCreate, user_id: int):
    db_comment = Comment(**comment.dict(), owner_id=user_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def get_comment(db: AsyncSession, comment_id: int):
    stmt = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_comments(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Comment).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def update_comment(db: AsyncSession, comment: CommentCreate, comment_id: int):
    stmt = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(stmt)
    db_comment = result.scalars().first()
    if db_comment:
        db_comment.content = comment.content
        await db.commit()
        await db.refresh(db_comment)
    return db_comment


async def delete_comment(db: AsyncSession, comment_id: int):
    stmt = select(Comment).filter(Comment.id == comment_id)
    result = await db.execute(stmt)
    db_comment = result.scalars().first()
    if db_comment:
        await db.delete(db_comment)
        await db.commit()
    return db_comment


async def create_auto_reply_setting(db: AsyncSession, auto_reply_setting: AutoReplySettingCreate, user_id: int):
    db_auto_reply_setting = AutoReplySetting(**auto_reply_setting.dict(), user_id=user_id)
    db.add(db_auto_reply_setting)
    await db.commit()
    await db.refresh(db_auto_reply_setting)
    return db_auto_reply_setting


async def get_auto_reply_setting(db: AsyncSession, auto_reply_setting_id: int):
    stmt = select(AutoReplySetting).filter(AutoReplySetting.id == auto_reply_setting_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def check_password(self, password: str) -> bool:
    return self.hashed_password == password


async def get_comments_daily_breakdown(db: AsyncSession, date_from: date, date_to: date):
    stmt = select(Comment).filter(Comment.created_at >= date_from, Comment.created_at <= date_to)
    result = await db.execute(stmt)
    comments = result.scalars().all()
    analytics = defaultdict(lambda: {'total_comments': 0, 'blocked_comments': 0})

    for comment in comments:
        comment_date = comment.created_at.date()
        analytics[comment_date]['total_comments'] += 1
        if comment.is_blocked:
            analytics[comment_date]['blocked_comments'] += 1

    return [{'date': date, **data} for date, data in analytics.items()]
