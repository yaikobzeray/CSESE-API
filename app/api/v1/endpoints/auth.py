from fastapi import APIRouter, HTTPException, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import admin as crud
from app.core.security import create_access_token
from app.schemas.admin import AdminCreate, AdminOut, AdminUpdate, LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: DbSession):
    admin = crud.authenticate_admin(db, data.email, data.password)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if not admin.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive account")
    token = create_access_token(admin.id)
    return Token(access_token=token)


@router.get("/me", response_model=AdminOut)
def get_me(current_admin: CurrentAdmin):
    return current_admin


@router.get("/admins", response_model=list[AdminOut])
def list_admins(db: DbSession, current_admin: CurrentAdmin):
    return crud.get_all_admins(db)


@router.post("/admins", response_model=AdminOut, status_code=status.HTTP_201_CREATED)
def create_admin(data: AdminCreate, db: DbSession, current_admin: CurrentAdmin):
    if crud.get_admin_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_admin(db, data)


@router.patch("/admins/{admin_id}", response_model=AdminOut)
def update_admin(admin_id: int, data: AdminUpdate, db: DbSession, current_admin: CurrentAdmin):
    admin = crud.get_admin_by_id(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return crud.update_admin(db, admin, data)


@router.delete("/admins/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(admin_id: int, db: DbSession, current_admin: CurrentAdmin):
    admin = crud.get_admin_by_id(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    crud.delete_admin(db, admin)
