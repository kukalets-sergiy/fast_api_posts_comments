from .routers import auth, posts, comments, analytics
from fastapi import FastAPI

app = FastAPI()


app.include_router(auth.router, prefix="/auth_user", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
