import enum

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class MembershipStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class SiteMember(Base):
    """Public membership registrations submitted via the website."""

    __tablename__ = "site_members"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Personal info
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Professional / Academic info
    occupation: Mapped[str | None] = mapped_column(String(255), nullable=True)   # e.g. "PhD Student", "Engineer"
    institution: Mapped[str | None] = mapped_column(String(255), nullable=True)
    field_of_study: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Motivation
    motivation: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Social links
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Admin-managed status
    status: Mapped[MembershipStatus] = mapped_column(
        Enum(MembershipStatus, name="membership_status"),
        default=MembershipStatus.pending,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
