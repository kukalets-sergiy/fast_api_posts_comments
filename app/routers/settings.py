# routers/settings.py
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.routers.auth import access_security
from app.schemas.auto_reply_setting import AutoReplySettingUpdate

router = APIRouter()


@router.put("/auto-reply-settings", response_model=AutoReplySettingUpdate)
def update_auto_reply_setting(
        settings: AutoReplySettingUpdate,
        db: Session = Depends(get_db),
        credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["id"]
    return crud.update_auto_reply_setting(db, user_id, settings)
