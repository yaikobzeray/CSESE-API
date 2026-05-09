from datetime import date

from pydantic import BaseModel

from app.models.job import JobStatus


class JobBase(BaseModel):
    title: str
    organization: str
    description: str | None = None
    status: JobStatus = JobStatus.open
    deadline: date | None = None
    external_url: str | None = None
    is_fellowship: bool = False
    is_published: bool = True


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = None
    organization: str | None = None
    description: str | None = None
    status: JobStatus | None = None
    deadline: date | None = None
    external_url: str | None = None
    is_fellowship: bool | None = None
    is_published: bool | None = None


class JobOut(JobBase):
    id: int

    model_config = {"from_attributes": True}
