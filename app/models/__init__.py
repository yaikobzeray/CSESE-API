# Re-export all models so that SQLAlchemy's metadata and Alembic can discover them
from app.models.admin import Admin  # noqa: F401
from app.models.award import Award, AwardRecipient  # noqa: F401
from app.models.contact import ContactSubmission, InterestSubmission  # noqa: F401
from app.models.event import Event  # noqa: F401
from app.models.job import Job  # noqa: F401
from app.models.member import Member  # noqa: F401
from app.models.site_member import SiteMember  # noqa: F401
from app.models.donation import DonationMethod, DonationMethodType  # noqa: F401
from app.models.news import News  # noqa: F401
