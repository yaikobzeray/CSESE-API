from pydantic import BaseModel, EmailStr

from app.models.contact import EducationLevel


class ContactSubmissionCreate(BaseModel):
    full_name: str
    email: EmailStr
    subject: str
    message: str


class ContactSubmissionOut(ContactSubmissionCreate):
    id: int
    is_read: bool

    model_config = {"from_attributes": True}


class InterestSubmissionCreate(BaseModel):
    full_name: str
    email: EmailStr
    education_level: EducationLevel
    motivation: str


class InterestSubmissionOut(InterestSubmissionCreate):
    id: int
    is_read: bool

    model_config = {"from_attributes": True}
