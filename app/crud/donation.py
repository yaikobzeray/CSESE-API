from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.donation import DonationMethod
from app.schemas.donation import DonationMethodCreate, DonationMethodUpdate


class CRUDDonationMethod:
    def get(self, db: Session, id: int) -> Optional[DonationMethod]:
        return db.get(DonationMethod, id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, active_only: bool = True
    ) -> List[DonationMethod]:
        query = select(DonationMethod).order_by(DonationMethod.display_order)
        if active_only:
            query = query.where(DonationMethod.is_active == True)
        return db.execute(query.offset(skip).limit(limit)).scalars().all()

    def create(self, db: Session, *, obj_in: DonationMethodCreate) -> DonationMethod:
        db_obj = DonationMethod(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: DonationMethod, obj_in: DonationMethodUpdate) -> DonationMethod:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> DonationMethod:
        obj = db.get(DonationMethod, id)
        db.delete(obj)
        db.commit()
        return obj


donation_method = CRUDDonationMethod()
