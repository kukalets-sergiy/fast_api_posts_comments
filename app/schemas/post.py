from app.schemas.user import OurBaseModel


class PostCreate(OurBaseModel):
    title: str
    content: str


class PostResponse(OurBaseModel):
    id: int
    title: str
    content: str
    owner_id: int
