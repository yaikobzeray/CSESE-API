from typing import Any, List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import DbSession

router = APIRouter()


@router.get("/methods", response_model=List[schemas.donation.DonationMethodOut])
def read_donation_methods(
    db: DbSession,
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve donation methods (Bank Accounts, Wallets)."""
    return crud.donation.donation_method.get_multi(
        db, skip=skip, limit=limit, active_only=True
    )


@router.get("/methods/{method_id}", response_model=schemas.donation.DonationMethodOut)
def read_donation_method_by_id(
    method_id: int,
    db: DbSession,
) -> Any:
    """Get donation method details by ID."""
    method = crud.donation.donation_method.get(db, id=method_id)
    if not method:
        raise HTTPException(status_code=404, detail="Donation method not found")
    return method
