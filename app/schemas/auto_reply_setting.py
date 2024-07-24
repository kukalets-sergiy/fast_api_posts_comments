from pydantic import BaseModel

class AutoReplySettingCreate(BaseModel):
    delay_seconds: int
    is_enabled: bool
