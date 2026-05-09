import enum

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class EducationLevel(str, enum.Enum):
    undergraduate = "Undergraduate"
    graduate = "Graduate"
    postgraduate = "Postgraduate"
    phd = "PhD"
    early_career = "Early Career Researcher"
    professional = "Professional"
    other = "Other"


class ContactSubmission(Base):
    """Messages submitted via the Contact form."""

    __tablename__ = "contact_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class InterestSubmission(Base):
    """Expressions of interest submitted via the Summer School form."""

    __tablename__ = "interest_submissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    education_level: Mapped[EducationLevel] = mapped_column(
        Enum(EducationLevel), nullable=False
    )
    motivation: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
