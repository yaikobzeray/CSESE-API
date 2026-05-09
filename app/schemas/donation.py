from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class DonationMethodType(str, Enum):
    BANK = "bank"
    WALLET = "wallet"


class DonationMethodBase(BaseModel):
    provider_name: str = Field(..., example="Commercial Bank of Ethiopia")
    account_name: str = Field("CSESE")
    account_number: str = Field(..., example="1000XXXXXXXXXX")
    currency: str = Field("ETB")
    method_type: DonationMethodType = DonationMethodType.BANK
    logo_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class DonationMethodCreate(DonationMethodBase):
    pass


class DonationMethodUpdate(DonationMethodBase):
    provider_name: Optional[str] = None
    account_number: Optional[str] = None


class DonationMethodOut(DonationMethodBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
