from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference
from sqladmin import Admin
from sqladmin.authentication import login_required
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.admin.auth import AdminAuthBackend
from app.admin.dashboard import get_dashboard_stats
from app.admin.views import (
    AdminView,
    AwardRecipientView,
    AwardView,
    ContactSubmissionView,
    DonationMethodView,
    EventView,
    InterestSubmissionView,
    JobView,
    MemberView,
    NewsView,
)
from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import SessionLocal, engine


def _seed_first_admin() -> None:
    """Create the first superadmin if no admins exist in the database."""
    from app.crud.admin import create_admin, get_admin_by_email
    from app.schemas.admin import AdminCreate

    db = SessionLocal()
    try:
        if get_admin_by_email(db, settings.FIRST_ADMIN_EMAIL):
            return  # Already seeded
        create_admin(
            db,
            AdminCreate(
                email=settings.FIRST_ADMIN_EMAIL,
                full_name="Super Admin",
                password=settings.FIRST_ADMIN_PASSWORD,
                is_active=True,
                is_superadmin=True,
            ),
        )
        print(f"[seed] First admin created: {settings.FIRST_ADMIN_EMAIL}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    _seed_first_admin()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

# --- Static files ---
Path("media").mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

Path("static").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- API Router ---
app.include_router(api_router, prefix=settings.API_V1_STR)

@login_required
async def _dashboard_index(self, request: Request) -> Response:
    """Override SQLAdmin home page to inject live stats."""
    from app.admin.dashboard import get_dashboard_stats

    stats = get_dashboard_stats()
    now = datetime.now().strftime("%d %b %Y, %H:%M")
    chart_labels = stats.pop("chart_labels")
    chart_news = stats.pop("chart_news")
    chart_events = stats.pop("chart_events")

    context = {
        "stats": stats,  # Jinja handles attributes of dicts
        "chart_labels": chart_labels,
        "chart_news": chart_news,
        "chart_events": chart_events,
        "now": now,
    }
    return await self.templates.TemplateResponse(request, "sqladmin/index.html", context)


# Apply monkey-patch to the class BEFORE instantiation
Admin.index = _dashboard_index

# --- SQLAdmin Panel ---
_auth_backend = AdminAuthBackend(secret_key=settings.SECRET_KEY)
admin_panel = Admin(
    app,
    engine=engine,
    authentication_backend=_auth_backend,
    title="CSESE Admin",
    base_url="/panel",
)
admin_panel.add_view(AdminView)
admin_panel.add_view(NewsView)
admin_panel.add_view(EventView)
admin_panel.add_view(JobView)
admin_panel.add_view(MemberView)
admin_panel.add_view(AwardView)
admin_panel.add_view(AwardRecipientView)
admin_panel.add_view(DonationMethodView)
admin_panel.add_view(ContactSubmissionView)
admin_panel.add_view(InterestSubmissionView)


# --- /admin redirect -> SQLAdmin panel ---
@app.get("/admin", include_in_schema=False)
@app.get("/admin/", include_in_schema=False)
async def admin_redirect() -> RedirectResponse:
    return RedirectResponse(url="/panel")


# --- Scalar API Docs ---
@app.get("/docs", include_in_schema=False)
async def scalar_docs() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


# --- Health Check ---
@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
    }

