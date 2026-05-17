from pydantic import BaseModel


class MemberBase(BaseModel):
    full_name: str
    title: str | None = None
    position: str | None = None
    institution: str | None = None
    bio: str | None = None
    linkedin_url: str | None = None
    profile_url: str | None = None
    avatar_url: str | None = None
    is_published: bool = True


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    full_name: str | None = None
    title: str | None = None
    position: str | None = None
    institution: str | None = None
    bio: str | None = None
    linkedin_url: str | None = None
    profile_url: str | None = None
    avatar_url: str | None = None
    is_published: bool | None = None


class MemberOut(MemberBase):
    id: int

    model_config = {"from_attributes": True}
