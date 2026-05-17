from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import site_member as crud
from app.models.site_member import MembershipStatus
from app.schemas.site_member import SiteMemberCreate, SiteMemberOut, SiteMemberUpdate

router = APIRouter(tags=["members"])


# ── Public ────────────────────────────────────────────────────────────────────

@router.post("/", response_model=SiteMemberOut, status_code=status.HTTP_201_CREATED)
def register_member(data: SiteMemberCreate, db: DbSession):
    """Submit a public membership registration. No authentication required."""
    existing = crud.get_site_member_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A registration with this email already exists.",
        )
    return crud.create_site_member(db, data)


# ── Admin-only ────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[SiteMemberOut])
def list_members(
    db: DbSession,
    _: CurrentAdmin,
    status_filter: MembershipStatus | None = None,
    skip: int = 0,
    limit: int = 50,
):
    """List all membership registrations. Admin only."""
    return crud.get_all_site_members(db, status=status_filter, skip=skip, limit=limit)


@router.get("/{member_id}", response_model=SiteMemberOut)
def get_member(member_id: int, db: DbSession, _: CurrentAdmin):
    """Fetch a single membership registration by ID. Admin only."""
    item = crud.get_site_member(db, member_id)
    if not item:
        raise HTTPException(status_code=404, detail="Member not found")
    return item


@router.patch("/{member_id}", response_model=SiteMemberOut)
def update_member(member_id: int, data: SiteMemberUpdate, db: DbSession, _: CurrentAdmin):
    """Update a membership registration (e.g. approve/reject). Admin only."""
    item = crud.get_site_member(db, member_id)
    if not item:
        raise HTTPException(status_code=404, detail="Member not found")
    return crud.update_site_member(db, item, data)


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: DbSession, _: CurrentAdmin):
    """Delete a membership registration. Admin only."""
    item = crud.get_site_member(db, member_id)
    if not item:
        raise HTTPException(status_code=404, detail="Member not found")
    crud.delete_site_member(db, item)
