from sqlalchemy.orm import Session

from app.models.site_member import MembershipStatus, SiteMember
from app.schemas.site_member import SiteMemberCreate, SiteMemberUpdate


def get_site_member(db: Session, member_id: int) -> SiteMember | None:
    return db.get(SiteMember, member_id)


def get_site_member_by_email(db: Session, email: str) -> SiteMember | None:
    return db.query(SiteMember).filter(SiteMember.email == email).first()


def get_all_site_members(
    db: Session,
    *,
    status: MembershipStatus | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[SiteMember]:
    q = db.query(SiteMember)
    if status:
        q = q.filter(SiteMember.status == status)
    return q.order_by(SiteMember.created_at.desc()).offset(skip).limit(limit).all()


def create_site_member(db: Session, data: SiteMemberCreate) -> SiteMember:
    member = SiteMember(**data.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


def update_site_member(db: Session, member: SiteMember, data: SiteMemberUpdate) -> SiteMember:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    db.commit()
    db.refresh(member)
    return member


def delete_site_member(db: Session, member: SiteMember) -> None:
    db.delete(member)
    db.commit()
