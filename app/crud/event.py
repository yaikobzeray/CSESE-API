from sqlalchemy.orm import Session

from app.models.event import Event, EventStatus
from app.schemas.event import EventCreate, EventUpdate


def get_event(db: Session, event_id: int) -> Event | None:
    return db.get(Event, event_id)


def get_all_events(
    db: Session,
    *,
    published_only: bool = True,
    status: EventStatus | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Event]:
    q = db.query(Event)
    if published_only:
        q = q.filter(Event.is_published == True)  # noqa: E712
    if status:
        q = q.filter(Event.status == status)
    return q.order_by(Event.event_date.desc()).offset(skip).limit(limit).all()


def create_event(db: Session, data: EventCreate) -> Event:
    event = Event(**data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def update_event(db: Session, event: Event, data: EventUpdate) -> Event:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, event: Event) -> None:
    db.delete(event)
    db.commit()
