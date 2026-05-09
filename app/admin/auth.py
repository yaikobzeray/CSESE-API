from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.core.security import create_access_token, decode_access_token


class AdminAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email = str(form.get("username", ""))
        password = str(form.get("password", ""))

        # Import here to avoid circular imports
        from app.crud.admin import authenticate_admin
        from app.db.session import SessionLocal

        db = SessionLocal()
        try:
            admin = authenticate_admin(db, email, password)
            if not admin:
                return False
            token = create_access_token(admin.id)
            request.session["admin_token"] = token
            return True
        finally:
            db.close()

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        token = request.session.get("admin_token")
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        subject = decode_access_token(token)
        if not subject:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        from app.crud.admin import get_admin_by_id
        from app.db.session import SessionLocal

        db = SessionLocal()
        try:
            admin = get_admin_by_id(db, int(subject))
            if not admin or not admin.is_active:
                return RedirectResponse(request.url_for("admin:login"), status_code=302)
        finally:
            db.close()

        return True
