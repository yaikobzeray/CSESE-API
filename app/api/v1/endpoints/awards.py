from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import award as crud
from app.schemas.award import AwardCreate, AwardOut, AwardRecipientCreate, AwardRecipientOut, AwardUpdate

router = APIRouter(tags=["Awards"])


@router.get("/", response_model=list[AwardOut])
def list_awards(db: DbSession):
    return crud.get_all_awards(db, published_only=True)


@router.get("/{award_id}", response_model=AwardOut)
def get_award(award_id: int, db: DbSession):
    item = crud.get_award(db, award_id)
    if not item:
        raise HTTPException(status_code=404, detail="Award not found")
    return item


@router.post("/", response_model=AwardOut, status_code=status.HTTP_201_CREATED)
def create_award(data: AwardCreate, db: DbSession, _: CurrentAdmin):
    return crud.create_award(db, data)


@router.patch("/{award_id}", response_model=AwardOut)
def update_award(award_id: int, data: AwardUpdate, db: DbSession, _: CurrentAdmin):
    item = crud.get_award(db, award_id)
    if not item:
        raise HTTPException(status_code=404, detail="Award not found")
    return crud.update_award(db, item, data)


@router.delete("/{award_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_award(award_id: int, db: DbSession, _: CurrentAdmin):
    item = crud.get_award(db, award_id)
    if not item:
        raise HTTPException(status_code=404, detail="Award not found")
    crud.delete_award(db, item)


# --- Recipients sub-resource ---
@router.post("/{award_id}/recipients", response_model=AwardRecipientOut, status_code=status.HTTP_201_CREATED)
def add_recipient(award_id: int, data: AwardRecipientCreate, db: DbSession, _: CurrentAdmin):
    if not crud.get_award(db, award_id):
        raise HTTPException(status_code=404, detail="Award not found")
    return crud.add_recipient(db, award_id, data)


@router.delete("/{award_id}/recipients/{recipient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipient(award_id: int, recipient_id: int, db: DbSession, _: CurrentAdmin):
    recipient = crud.get_recipient(db, recipient_id)
    if not recipient or recipient.award_id != award_id:
        raise HTTPException(status_code=404, detail="Recipient not found")
    crud.delete_recipient(db, recipient)
