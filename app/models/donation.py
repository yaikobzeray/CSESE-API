from sqlalchemy import Boolean, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.db.base import Base


class DonationMethodType(str, enum.Enum):
    BANK = "bank"
    WALLET = "wallet"


class DonationMethod(Base):
    """Dynamic donation methods (Bank Accounts, Mobile Wallets)."""

    __tablename__ = "donation_methods"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    provider_name: Mapped[str] = mapped_column(String(255), nullable=False) # e.g. Commercial Bank of Ethiopia
    account_name: Mapped[str] = mapped_column(String(255), default="CSESE") 
    account_number: Mapped[str] = mapped_column(String(255), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="ETB")
    
    # Use real Enum type for better admin support
    method_type: Mapped[DonationMethodType] = mapped_column(Enum(DonationMethodType), default=DonationMethodType.BANK, nullable=False)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    display_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
