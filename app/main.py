from fastapi import FastAPI
from .routers import auth, posts, comments
import logging

logging.basicConfig(level=logging.DEBUG)


app = FastAPI()


app.include_router(auth.router, prefix="/auth_user", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
