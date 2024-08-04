from app.config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
from app.database import SessionLocal
from app.models.comment import Comment
from app.models.post import Post
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
                reply_content = generate_relevant_reply(post, comment)

                new_comment = Comment(
                    content=reply_content,
                    post_id=post_id,
                    parent_comment_id=comment_id,
                    owner_id=post.owner_id,
                    is_blocked=False
                )

                db.add(new_comment)
                db.commit()
                db.refresh(new_comment)
    finally:
        db.close()


def generate_relevant_reply(post: Post, comment: Comment) -> str:
    if comment.is_blocked:
        return f"Thank you for your comment on '{post.title}'. We noticed your concern and will address it promptly."
    else:
        return f"Thank you for your positive feedback on '{post.title}'. We appreciate your input!"
