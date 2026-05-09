from sqlalchemy.orm import Session

from app.models.contact import ContactSubmission, InterestSubmission
from app.schemas.contact import ContactSubmissionCreate, InterestSubmissionCreate


def create_contact(db: Session, data: ContactSubmissionCreate) -> ContactSubmission:
    submission = ContactSubmission(**data.model_dump())
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def get_all_contacts(db: Session, *, unread_only: bool = False) -> list[ContactSubmission]:
    q = db.query(ContactSubmission)
    if unread_only:
        q = q.filter(ContactSubmission.is_read == False)  # noqa: E712
    return q.order_by(ContactSubmission.created_at.desc()).all()


def mark_contact_read(db: Session, submission: ContactSubmission) -> ContactSubmission:
    submission.is_read = True
    db.commit()
    db.refresh(submission)
    return submission


def create_interest(db: Session, data: InterestSubmissionCreate) -> InterestSubmission:
    submission = InterestSubmission(**data.model_dump())
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def get_all_interests(db: Session, *, unread_only: bool = False) -> list[InterestSubmission]:
    q = db.query(InterestSubmission)
    if unread_only:
        q = q.filter(InterestSubmission.is_read == False)  # noqa: E712
    return q.order_by(InterestSubmission.created_at.desc()).all()


def mark_interest_read(db: Session, submission: InterestSubmission) -> InterestSubmission:
    submission.is_read = True
    db.commit()
    db.refresh(submission)
    return submission
