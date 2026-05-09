"""
Seed script — creates the first superadmin from .env settings.
Run once: python -m app.utils.seed_admin
"""

from app.core.config import settings
from app.crud.admin import create_admin, get_admin_by_email
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.schemas.admin import AdminCreate


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = get_admin_by_email(db, settings.FIRST_ADMIN_EMAIL)
        if existing:
            print(f"✅ Admin already exists: {settings.FIRST_ADMIN_EMAIL}")
            return

        admin = create_admin(
            db,
            AdminCreate(
                email=settings.FIRST_ADMIN_EMAIL,
                full_name="Super Admin",
                password=settings.FIRST_ADMIN_PASSWORD,
                is_active=True,
                is_superadmin=True,
            ),
        )
        print(f"🎉 Created superadmin: {admin.email}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
