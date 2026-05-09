from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Award(Base):
    """Awards defined by CSESE (e.g. Outstanding Service, FaST Award)."""

    __tablename__ = "awards"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    eligibility: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationship to past recipients
    recipients: Mapped[list["AwardRecipient"]] = relationship(
        "AwardRecipient", back_populates="award", cascade="all, delete-orphan"
    )


class AwardRecipient(Base):
    """Past recipients of a specific award."""

    __tablename__ = "award_recipients"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    award_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("awards.id", ondelete="CASCADE"), nullable=False
    )
    recipient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    institution: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    award: Mapped["Award"] = relationship("Award", back_populates="recipients")
