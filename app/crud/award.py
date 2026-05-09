from sqlalchemy.orm import Session

from app.models.award import Award, AwardRecipient
from app.schemas.award import AwardCreate, AwardRecipientCreate, AwardUpdate


def get_award(db: Session, award_id: int) -> Award | None:
    return db.get(Award, award_id)


def get_all_awards(
    db: Session,
    *,
    published_only: bool = True,
) -> list[Award]:
    q = db.query(Award)
    if published_only:
        q = q.filter(Award.is_published == True)  # noqa: E712
    return q.order_by(Award.title).all()


def create_award(db: Session, data: AwardCreate) -> Award:
    award = Award(**data.model_dump())
    db.add(award)
    db.commit()
    db.refresh(award)
    return award


def update_award(db: Session, award: Award, data: AwardUpdate) -> Award:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(award, field, value)
    db.commit()
    db.refresh(award)
    return award


def delete_award(db: Session, award: Award) -> None:
    db.delete(award)
    db.commit()


# --- Recipients ---
def add_recipient(db: Session, award_id: int, data: AwardRecipientCreate) -> AwardRecipient:
    recipient = AwardRecipient(award_id=award_id, **data.model_dump())
    db.add(recipient)
    db.commit()
    db.refresh(recipient)
    return recipient


def delete_recipient(db: Session, recipient: AwardRecipient) -> None:
    db.delete(recipient)
    db.commit()


def get_recipient(db: Session, recipient_id: int) -> AwardRecipient | None:
    return db.get(AwardRecipient, recipient_id)
