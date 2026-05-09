from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate


def get_admin_by_id(db: Session, admin_id: int) -> Admin | None:
    return db.get(Admin, admin_id)


def get_admin_by_email(db: Session, email: str) -> Admin | None:
    return db.query(Admin).filter(Admin.email == email).first()


def get_all_admins(db: Session) -> list[Admin]:
    return db.query(Admin).all()


def create_admin(db: Session, data: AdminCreate) -> Admin:
    admin = Admin(
        email=data.email,
        full_name=data.full_name,
        hashed_password=hash_password(data.password),
        is_active=data.is_active,
        is_superadmin=data.is_superadmin,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def update_admin(db: Session, admin: Admin, data: AdminUpdate) -> Admin:
    update_data = data.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    for field, value in update_data.items():
        setattr(admin, field, value)
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin: Admin) -> None:
    db.delete(admin)
    db.commit()


def authenticate_admin(db: Session, email: str, password: str) -> Admin | None:
    admin = get_admin_by_email(db, email)
    if not admin or not verify_password(password, admin.hashed_password):
        return None
    return admin
