from pydantic import BaseModel


class AwardRecipientBase(BaseModel):
    recipient_name: str
    year: int
    institution: str | None = None
    notes: str | None = None


class AwardRecipientCreate(AwardRecipientBase):
    pass


class AwardRecipientOut(AwardRecipientBase):
    id: int
    award_id: int

    model_config = {"from_attributes": True}


class AwardBase(BaseModel):
    title: str
    description: str
    eligibility: str | None = None
    is_published: bool = True


class AwardCreate(AwardBase):
    pass


class AwardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    eligibility: str | None = None
    is_published: bool | None = None


class AwardOut(AwardBase):
    id: int
    recipients: list[AwardRecipientOut] = []

    model_config = {"from_attributes": True}
