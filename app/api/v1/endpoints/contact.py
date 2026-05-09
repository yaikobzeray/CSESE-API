from fastapi import APIRouter, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import contact as crud
from app.schemas.contact import (
    ContactSubmissionCreate,
    ContactSubmissionOut,
    InterestSubmissionCreate,
    InterestSubmissionOut,
)

router = APIRouter(tags=["Contact & Interest Forms"])


# --- Contact form (public) ---
@router.post("/", response_model=ContactSubmissionOut, status_code=status.HTTP_201_CREATED)
def submit_contact(data: ContactSubmissionCreate, db: DbSession):
    return crud.create_contact(db, data)


@router.get("/", response_model=list[ContactSubmissionOut])
def list_contacts(db: DbSession, _: CurrentAdmin, unread_only: bool = False):
    return crud.get_all_contacts(db, unread_only=unread_only)


@router.patch("/{submission_id}/read", response_model=ContactSubmissionOut)
def mark_contact_read(submission_id: int, db: DbSession, _: CurrentAdmin):
    from app.models.contact import ContactSubmission
    sub = db.get(ContactSubmission, submission_id)
    if not sub:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Submission not found")
    return crud.mark_contact_read(db, sub)


# --- Summer school interest form (public) ---
@router.post("/interest", response_model=InterestSubmissionOut, status_code=status.HTTP_201_CREATED)
def submit_interest(data: InterestSubmissionCreate, db: DbSession):
    return crud.create_interest(db, data)


@router.get("/interest", response_model=list[InterestSubmissionOut])
def list_interests(db: DbSession, _: CurrentAdmin, unread_only: bool = False):
    return crud.get_all_interests(db, unread_only=unread_only)


@router.patch("/interest/{submission_id}/read", response_model=InterestSubmissionOut)
def mark_interest_read(submission_id: int, db: DbSession, _: CurrentAdmin):
    from app.models.contact import InterestSubmission
    sub = db.get(InterestSubmission, submission_id)
    if not sub:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Submission not found")
    return crud.mark_interest_read(db, sub)
