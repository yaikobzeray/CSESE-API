from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import member as crud
from app.schemas.member import MemberCreate, MemberOut, MemberUpdate

router = APIRouter(tags=["Who is Who"])


@router.get("/", response_model=list[MemberOut])
def list_members(db: DbSession):
    return crud.get_all_members(db, published_only=True)


@router.get("/{member_id}", response_model=MemberOut)
def get_member(member_id: int, db: DbSession):
    item = crud.get_member(db, member_id)
    if not item:
        raise HTTPException(status_code=404, detail="Member not found")
    return item


@router.post("/", response_model=MemberOut, status_code=status.HTTP_201_CREATED)
def create_member(data: MemberCreate, db: DbSession, _: CurrentAdmin):
    return crud.create_member(db, data)


@router.patch("/{member_id}", response_model=MemberOut)
def update_member(member_id: int, data: MemberUpdate, db: DbSession, _: CurrentAdmin):
    item = crud.get_member(db, member_id)
    if not item:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.update_member(db, item, data)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: DbSession, _: CurrentAdmin):
    item = crud.get_member(db, member_id)
    if not item:
        raise HTTPException(status_code=404, detail="Member not found")
    crud.delete_member(db, item)
