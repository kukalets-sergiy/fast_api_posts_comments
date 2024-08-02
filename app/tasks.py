from app import crud
from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from app.database import SessionLocal
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import CommentCreate

# tasks.py
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND


@celery.task(name="app.tasks.simple_task")
def simple_task():
    print("Simple task executed!")
    return "Task complete"


@celery.task(name="app.tasks.auto_reply_task")
def auto_reply_task(post_id: int, comment_id: int):
    db = SessionLocal()
    try:
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if comment:
            post = db.query(Post).filter(Post.id == post_id).first()
            if post:
                user_setting = crud.get_auto_reply_setting(db, post.owner_id)
                if user_setting and user_setting.is_enabled:
                    reply_content = generate_relevant_reply(post, comment)
                    new_comment = CommentCreate(
                        content=reply_content,
                        post_id=post_id,
                        parent_comment_id=comment_id
                    )
                    crud.create_comment(db, new_comment, post.owner_id, is_blocked=False)
    finally:
        db.close()


def generate_relevant_reply(post: Post, comment: Comment) -> str:
    # A simple example of generating a relevant response
    return f"Thank you for your comment on '{post.title}'. Your feedback is appreciated!"
