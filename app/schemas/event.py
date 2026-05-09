from datetime import date

from pydantic import BaseModel

from app.models.event import EventStatus


class EventBase(BaseModel):
    title: str
    description: str
    location: str
    event_date: date
    end_date: date | None = None
    status: EventStatus = EventStatus.upcoming
    registration_url: str | None = None
    image_url: str | None = None
    is_published: bool = True


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    event_date: date | None = None
    end_date: date | None = None
    status: EventStatus | None = None
    registration_url: str | None = None
    image_url: str | None = None
    is_published: bool | None = None


class EventOut(EventBase):
    id: int

    model_config = {"from_attributes": True}
