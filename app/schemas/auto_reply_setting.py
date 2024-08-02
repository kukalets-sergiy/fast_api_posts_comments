from app.schemas.user import OurBaseModel


class AutoReplySettingCreate(OurBaseModel):
    id: int
    user_id: int
    delay_seconds: int
    is_enabled: bool
