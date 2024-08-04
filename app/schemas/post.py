from app.schemas.user import OurBaseModel


class PostCreate(OurBaseModel):
    title: str
    content: str
    auto_reply_enabled: bool = False
    auto_reply_delay: int = 2


class PostResponse(OurBaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    auto_reply_enabled: bool = False
    auto_reply_delay: int = 2
