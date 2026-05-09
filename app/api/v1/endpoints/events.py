from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import event as crud
from app.models.event import EventStatus
from app.schemas.event import EventCreate, EventOut, EventUpdate

router = APIRouter(tags=["Events"])


@router.get("/", response_model=list[EventOut])
def list_events(
    db: DbSession,
    event_status: Annotated[EventStatus | None, Query(alias="status")] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 20,
):
    return crud.get_all_events(db, published_only=True, status=event_status, skip=skip, limit=limit)


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: DbSession):
    item = crud.get_event(db, event_id)
    if not item:
        raise HTTPException(status_code=404, detail="Event not found")
    return item


@router.post("/", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(data: EventCreate, db: DbSession, _: CurrentAdmin):
    return crud.create_event(db, data)


@router.patch("/{event_id}", response_model=EventOut)
def update_event(event_id: int, data: EventUpdate, db: DbSession, _: CurrentAdmin):
    item = crud.get_event(db, event_id)
    if not item:
        raise HTTPException(status_code=404, detail="Event not found")
    return crud.update_event(db, item, data)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: DbSession, _: CurrentAdmin):
    item = crud.get_event(db, event_id)
    if not item:
        raise HTTPException(status_code=404, detail="Event not found")
    crud.delete_event(db, item)
