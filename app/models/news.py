import enum

from sqlalchemy import Boolean, Date, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class NewsCategory(str, enum.Enum):
    announcement = "Announcement"
    award = "Award"
    event = "Event"
    general = "General"


class News(Base):
    """News and announcements published on the website."""

    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[NewsCategory] = mapped_column(
        Enum(NewsCategory), default=NewsCategory.general, nullable=False
    )
    publish_date: Mapped[str] = mapped_column(Date, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    read_more_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
