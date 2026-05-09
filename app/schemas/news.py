from datetime import date

from pydantic import BaseModel

from app.models.news import NewsCategory


class NewsBase(BaseModel):
    title: str
    summary: str
    content: str | None = None
    category: NewsCategory = NewsCategory.general
    publish_date: date
    image_url: str | None = None
    read_more_url: str | None = None
    is_published: bool = True


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: str | None = None
    summary: str | None = None
    content: str | None = None
    category: NewsCategory | None = None
    publish_date: date | None = None
    image_url: str | None = None
    read_more_url: str | None = None
    is_published: bool | None = None


class NewsOut(NewsBase):
    id: int

    model_config = {"from_attributes": True}
