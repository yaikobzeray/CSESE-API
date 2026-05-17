"""Dashboard stats injected into the sqladmin home page (sqladmin/index.html override)."""
from datetime import date, timedelta

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.admin import Admin
from app.models.award import Award, AwardRecipient
from app.models.contact import ContactSubmission, InterestSubmission
from app.models.event import Event
from app.models.job import Job
from app.models.member import Member
from app.models.site_member import MembershipStatus, SiteMember
from app.models.donation import DonationMethod
from app.models.news import News


def get_dashboard_stats() -> dict:
    """Query all dashboard statistics synchronously."""
    db = SessionLocal()
    try:
        today = date.today()

        # ── KPI counts ──────────────────────────────────────────────────────
        total_news       = db.scalar(select(func.count()).select_from(News))
        published_news   = db.scalar(select(func.count()).select_from(News).where(News.is_published == True))

        total_events     = db.scalar(select(func.count()).select_from(Event))
        upcoming_events  = db.scalar(select(func.count()).select_from(Event).where(Event.event_date >= today))

        total_jobs       = db.scalar(select(func.count()).select_from(Job))
        active_jobs      = db.scalar(select(func.count()).select_from(Job).where(Job.status == "open"))

        total_members    = db.scalar(select(func.count()).select_from(Member))
        published_members = db.scalar(select(func.count()).select_from(Member).where(Member.is_published == True))

        total_awards     = db.scalar(select(func.count()).select_from(Award))
        total_recipients = db.scalar(select(func.count()).select_from(AwardRecipient))

        # Donation stats
        total_methods    = db.scalar(select(func.count()).select_from(DonationMethod))
        active_methods   = db.scalar(select(func.count()).select_from(DonationMethod).where(DonationMethod.is_active == True))

        total_contacts   = db.scalar(select(func.count()).select_from(ContactSubmission))
        unread_contacts  = db.scalar(select(func.count()).select_from(ContactSubmission).where(ContactSubmission.is_read == False))

        total_interests  = db.scalar(select(func.count()).select_from(InterestSubmission))
        unread_interests = db.scalar(select(func.count()).select_from(InterestSubmission).where(InterestSubmission.is_read == False))

        total_applications  = db.scalar(select(func.count()).select_from(SiteMember))
        pending_applications = db.scalar(select(func.count()).select_from(SiteMember).where(SiteMember.status == MembershipStatus.pending))
        approved_applications = db.scalar(select(func.count()).select_from(SiteMember).where(SiteMember.status == MembershipStatus.approved))

        total_admins     = db.scalar(select(func.count()).select_from(Admin))

        # ── Recent activity ────────────────────────────────────────────────
        recent_contacts = db.execute(
            select(ContactSubmission).order_by(ContactSubmission.created_at.desc()).limit(5)
        ).scalars().all()

        recent_news = db.execute(
            select(News).order_by(News.created_at.desc()).limit(5)
        ).scalars().all()

        # ── Chart data (6 months) ──────────────────────────────────────────
        months_labels, months_news, months_events = [], [], []
        for i in range(5, -1, -1):
            m_start = date(today.year, today.month, 1) - timedelta(days=i * 30)
            m_end = m_start + timedelta(days=30)
            months_labels.append(m_start.strftime("%b %Y"))
            months_news.append(db.scalar(select(func.count()).select_from(News).where(News.created_at >= m_start, News.created_at < m_end)) or 0)
            months_events.append(db.scalar(select(func.count()).select_from(Event).where(Event.created_at >= m_start, News.created_at < m_end)) or 0)

        return {
            "total_news": total_news or 0,
            "published_news": published_news or 0,
            "draft_news": (total_news or 0) - (published_news or 0),
            "total_events": total_events or 0,
            "upcoming_events": upcoming_events or 0,
            "total_jobs": total_jobs or 0,
            "active_jobs": active_jobs or 0,
            "total_members": total_members or 0,
            "published_members": published_members or 0,
            "total_awards": total_awards or 0,
            "total_recipients": total_recipients or 0,
            "total_methods": total_methods or 0,
            "active_methods": active_methods or 0,
            "total_contacts": total_contacts or 0,
            "unread_contacts": unread_contacts or 0,
            "total_interests": total_interests or 0,
            "unread_interests": unread_interests or 0,
            "total_applications": total_applications or 0,
            "pending_applications": pending_applications or 0,
            "approved_applications": approved_applications or 0,
            "total_admins": total_admins or 0,
            "recent_contacts": recent_contacts,
            "recent_news": recent_news,
            "chart_labels": months_labels,
            "chart_news": months_news,
            "chart_events": months_events,
        }
    finally:
        db.close()
