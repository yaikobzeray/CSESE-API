from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_superadmin: bool = False


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    full_name: str | None = None
    password: str | None = None
    is_active: bool | None = None


class AdminOut(AdminBase):
    id: int

    model_config = {"from_attributes": True}


# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
