from app.schemas.user import OurBaseModel


class AutoReplySettingCreate(OurBaseModel):
    delay_seconds: int
    is_enabled: bool
