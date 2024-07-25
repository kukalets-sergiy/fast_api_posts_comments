from fastapi import FastAPI
from fastapi_jwt import JwtAccessBearer
from .config import settings
from .routers import auth, posts, comments
import logging

logging.basicConfig(level=logging.DEBUG)


app = FastAPI()

access_security = JwtAccessBearer(secret_key=settings.secret_key, auto_error=True)

app.include_router(auth.router, prefix="/auth_user", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
