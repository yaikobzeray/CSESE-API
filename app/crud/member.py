from sqlalchemy.orm import Session

from app.models.member import Member
from app.schemas.member import MemberCreate, MemberUpdate


def get_member(db: Session, member_id: int) -> Member | None:
    return db.get(Member, member_id)


def get_all_members(
    db: Session,
    *,
    published_only: bool = True,
    skip: int = 0,
    limit: int = 50,
) -> list[Member]:
    q = db.query(Member)
    if published_only:
        q = q.filter(Member.is_published == True)  # noqa: E712
    return q.order_by(Member.full_name).offset(skip).limit(limit).all()


def create_member(db: Session, data: MemberCreate) -> Member:
    member = Member(**data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def update_member(db: Session, member: Member, data: MemberUpdate) -> Member:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    db.commit()
    db.refresh(member)
    return member


def delete_member(db: Session, member: Member) -> None:
    db.delete(member)
    db.commit()
