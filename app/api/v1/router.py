from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    awards,
    contact,
    donation,
    events,
    jobs,
    members,
    news,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(members.router, prefix="/members", tags=["members"])
api_router.include_router(awards.router, prefix="/awards", tags=["awards"])
api_router.include_router(donation.router, prefix="/donation", tags=["donation"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
