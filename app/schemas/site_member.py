from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.site_member import MembershipStatus


class SiteMemberBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str | None = None
    nationality: str | None = None
    occupation: str | None = None
    institution: str | None = None
    field_of_study: str | None = None
    motivation: str | None = None
    linkedin_url: str | None = None


class SiteMemberCreate(SiteMemberBase):
    pass


class SiteMemberUpdate(BaseModel):
    """Admin-only update: change status or active flag."""
    status: MembershipStatus | None = None
    is_active: bool | None = None
    # Allow admin to also correct personal fields if needed
    full_name: str | None = None
    phone: str | None = None
    nationality: str | None = None
    occupation: str | None = None
    institution: str | None = None
    field_of_study: str | None = None
    motivation: str | None = None
    linkedin_url: str | None = None


class SiteMemberOut(SiteMemberBase):
    id: int
    status: MembershipStatus
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
