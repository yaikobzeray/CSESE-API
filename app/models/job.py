import enum

from sqlalchemy import Boolean, Date, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class JobStatus(str, enum.Enum):
    open = "Open"
    closed = "Closed"
    expired = "Expired"


class Job(Base):
    """Jobs and fellowship opportunities posted on the website."""

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    organization: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus), default=JobStatus.open, nullable=False
    )
    deadline: Mapped[str | None] = mapped_column(Date, nullable=True)
    external_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    is_fellowship: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
