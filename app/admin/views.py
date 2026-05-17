from pathlib import Path
from typing import Any, List, Type
from uuid import uuid4

from sqladmin import ModelView
from sqladmin.filters import AllUniqueStringValuesFilter, BooleanFilter
from starlette.requests import Request
from wtforms import FileField, Form, PasswordField, SelectField
from wtforms.validators import Optional


async def _save_upload(request: Request, field_name: str, subfolder: str = "images") -> str | None:
    """Save an uploaded file and return its served URL, or None if no file uploaded."""
    form = await request.form()
    upload = form.get(field_name)
    if not upload or not getattr(upload, "filename", None):
        return None
    suffix = Path(upload.filename).suffix.lower() or ".jpg"
    filename = f"{uuid4().hex}{suffix}"
    dest = Path("media") / subfolder / filename
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(await upload.read())
    return f"/media/{subfolder}/{filename}"

from app.models.admin import Admin
from app.models.award import Award, AwardRecipient
from app.models.contact import ContactSubmission, InterestSubmission
from app.models.event import Event
from app.models.job import Job
from app.models.member import Member
from app.models.site_member import SiteMember, MembershipStatus
from app.models.donation import DonationMethod
from app.models.news import News


# ---------------------------------------------------------------------------
# Administration
# ---------------------------------------------------------------------------

class AdminView(ModelView, model=Admin):
    name = "Admin User"
    name_plural = "Admin Users"
    icon = "fa-solid fa-user-shield"
    category = "Administration"

    column_list = [Admin.id, Admin.full_name, Admin.email, Admin.is_active, Admin.is_superadmin, Admin.created_at]
    column_searchable_list = [Admin.full_name, Admin.email]
    column_sortable_list = [Admin.full_name, Admin.email, Admin.is_active, Admin.is_superadmin, Admin.created_at]
    column_default_sort = [(Admin.created_at, True)]
    column_filters = [BooleanFilter(Admin.is_active), BooleanFilter(Admin.is_superadmin)]
    column_details_list = [Admin.id, Admin.full_name, Admin.email, Admin.is_active, Admin.is_superadmin, Admin.created_at, Admin.updated_at]

    can_view_details = True
    page_size = 20

    async def scaffold_form(self, rules: List[str] | None = None) -> Type[Form]:
        form_class = await super().scaffold_form(rules)
        form_class.password = PasswordField("Password", validators=[Optional()], description="Leave empty to keep existing password")
        return form_class

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        from app.core.security import hash_password
        if data.get("password"):
            model.hashed_password = hash_password(data["password"])


# ---------------------------------------------------------------------------
# Content – News
# ---------------------------------------------------------------------------

class NewsView(ModelView, model=News):
    name = "Article"
    name_plural = "News"
    icon = "fa-solid fa-newspaper"
    category = "Content"

    column_list = [News.id, News.title, News.category, News.is_published, News.created_at]
    column_searchable_list = [News.title, News.content]
    column_sortable_list = [News.title, News.category, News.is_published, News.created_at]
    column_default_sort = [(News.created_at, True)]
    column_filters = [AllUniqueStringValuesFilter(News.category), BooleanFilter(News.is_published)]
    column_details_list = [News.id, News.title, News.summary, News.content, News.category, News.publish_date, News.image_url, News.read_more_url, News.is_published, News.created_at, News.updated_at]
    form_columns = [News.title, News.summary, News.content, News.category, News.publish_date, News.read_more_url, News.is_published]

    can_view_details = True
    page_size = 25
    page_size_options = [10, 25, 50, 100]

    async def scaffold_form(self, rules: List[str] | None = None) -> Type[Form]:
        form_class = await super().scaffold_form(rules)
        form_class.image = FileField("Feature Image", validators=[Optional()], description="Upload a high-quality news image")
        return form_class

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        url = await _save_upload(request, "image", subfolder="images")
        if url:
            model.image_url = url


# ---------------------------------------------------------------------------
# Content – Events
# ---------------------------------------------------------------------------

class EventView(ModelView, model=Event):
    name = "Event"
    name_plural = "Events"
    icon = "fa-solid fa-calendar-days"
    category = "Content"

    column_list = [Event.id, Event.title, Event.event_date, Event.location, Event.is_published]
    column_searchable_list = [Event.title, Event.location]
    column_sortable_list = [Event.title, Event.event_date, Event.is_published]
    column_default_sort = [(Event.event_date, True)]
    column_filters = [BooleanFilter(Event.is_published)]
    column_details_list = [Event.id, Event.title, Event.description, Event.event_date, Event.location, Event.image_url, Event.registration_url, Event.is_published, Event.created_at, Event.updated_at]
    form_columns = [Event.title, Event.description, Event.event_date, Event.location, Event.registration_url, Event.is_published]

    can_view_details = True
    page_size = 20

    async def scaffold_form(self, rules: List[str] | None = None) -> Type[Form]:
        form_class = await super().scaffold_form(rules)
        form_class.image = FileField("Event Banner", validators=[Optional()])
        return form_class

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        url = await _save_upload(request, "image", subfolder="images")
        if url:
            model.image_url = url


# ---------------------------------------------------------------------------
# Content – Jobs
# ---------------------------------------------------------------------------

class JobView(ModelView, model=Job):
    name = "Job"
    name_plural = "Jobs & Fellowships"
    icon = "fa-solid fa-briefcase"
    category = "Content"

    column_list = [Job.id, Job.title, Job.organization, Job.is_fellowship, Job.status, Job.deadline, Job.is_published, Job.created_at]
    column_searchable_list = [Job.title, Job.organization]
    column_sortable_list = [Job.title, Job.organization, Job.status, Job.deadline, Job.is_fellowship, Job.is_published, Job.created_at]
    column_default_sort = [(Job.created_at, True)]
    column_filters = [AllUniqueStringValuesFilter(Job.status), BooleanFilter(Job.is_fellowship), BooleanFilter(Job.is_published)]
    column_details_list = [Job.id, Job.title, Job.organization, Job.description, Job.status, Job.deadline, Job.external_url, Job.is_fellowship, Job.is_published, Job.created_at, Job.updated_at]
    form_columns = [Job.title, Job.organization, Job.description, Job.status, Job.deadline, Job.external_url, Job.is_fellowship, Job.is_published]

    can_view_details = True
    page_size = 25


# ---------------------------------------------------------------------------
# Content – Members (Who is Who)
# ---------------------------------------------------------------------------

class MemberView(ModelView, model=Member):
    name = "Member"
    name_plural = "Who is Who"
    icon = "fa-solid fa-users"
    category = "Content"

    column_list = [Member.id, Member.full_name, Member.title, Member.position, Member.institution, Member.is_published]
    column_searchable_list = [Member.full_name, Member.institution, Member.position]
    column_sortable_list = [Member.full_name, Member.institution, Member.position, Member.is_published]
    column_default_sort = [(Member.full_name, False)]
    column_filters = [BooleanFilter(Member.is_published)]
    column_details_list = [Member.id, Member.full_name, Member.title, Member.position, Member.institution, Member.bio, Member.linkedin_url, Member.profile_url, Member.avatar_url, Member.is_published, Member.created_at, Member.updated_at]
    form_columns = [Member.full_name, Member.title, Member.position, Member.institution, Member.bio, Member.linkedin_url, Member.profile_url, Member.is_published]

    can_view_details = True
    page_size = 25

    async def scaffold_form(self, rules: List[str] | None = None) -> Type[Form]:
        form_class = await super().scaffold_form(rules)
        form_class.avatar = FileField("Avatar / Profile Photo", validators=[Optional()])
        return form_class

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        url = await _save_upload(request, "avatar", subfolder="avatars")
        if url:
            model.avatar_url = url


# ---------------------------------------------------------------------------
# Content – Site Members (Public Registrations)
# ---------------------------------------------------------------------------

class SiteMemberView(ModelView, model=SiteMember):
    name = "Member Application"
    name_plural = "Member Applications"
    icon = "fa-solid fa-id-card"
    category = "Submissions"

    column_list = [
        SiteMember.id,
        SiteMember.full_name,
        SiteMember.email,
        SiteMember.occupation,
        SiteMember.institution,
        SiteMember.status,
        SiteMember.created_at,
    ]
    column_searchable_list = [SiteMember.full_name, SiteMember.email, SiteMember.institution]
    column_sortable_list = [SiteMember.full_name, SiteMember.status, SiteMember.created_at]
    column_default_sort = [(SiteMember.created_at, True)]
    column_filters = [
        AllUniqueStringValuesFilter(SiteMember.status),
        BooleanFilter(SiteMember.is_active),
    ]
    column_details_list = [
        SiteMember.id,
        SiteMember.full_name,
        SiteMember.email,
        SiteMember.phone,
        SiteMember.nationality,
        SiteMember.occupation,
        SiteMember.institution,
        SiteMember.field_of_study,
        SiteMember.motivation,
        SiteMember.linkedin_url,
        SiteMember.status,
        SiteMember.is_active,
        SiteMember.created_at,
    ]
    form_columns = [SiteMember.status, SiteMember.is_active]

    can_create = False  # Applications are submitted via the public form
    can_view_details = True
    page_size = 30


# ---------------------------------------------------------------------------
# Content – Awards
# ---------------------------------------------------------------------------

class AwardView(ModelView, model=Award):
    name = "Award"
    name_plural = "Awards"
    icon = "fa-solid fa-trophy"
    category = "Content"

    column_list = [Award.id, Award.title, Award.is_published, Award.created_at]
    column_searchable_list = [Award.title]
    column_sortable_list = [Award.title, Award.is_published, Award.created_at]
    column_default_sort = [(Award.title, False)]
    column_filters = [BooleanFilter(Award.is_published)]
    column_details_list = [Award.id, Award.title, Award.description, Award.eligibility, Award.is_published, Award.created_at, Award.updated_at]
    form_columns = [Award.title, Award.description, Award.eligibility, Award.is_published]

    can_view_details = True
    page_size = 20


class AwardRecipientView(ModelView, model=AwardRecipient):
    name = "Award Recipient"
    name_plural = "Award Recipients"
    icon = "fa-solid fa-medal"
    category = "Content"

    column_list = [AwardRecipient.id, AwardRecipient.award_id, AwardRecipient.recipient_name, AwardRecipient.year, AwardRecipient.institution]
    column_searchable_list = [AwardRecipient.recipient_name, AwardRecipient.institution]
    column_sortable_list = [AwardRecipient.year, AwardRecipient.recipient_name, AwardRecipient.institution]
    column_details_list = [AwardRecipient.id, AwardRecipient.award_id, AwardRecipient.recipient_name, AwardRecipient.year, AwardRecipient.institution, AwardRecipient.notes, AwardRecipient.created_at, AwardRecipient.updated_at]
    form_columns = [AwardRecipient.award_id, AwardRecipient.recipient_name, AwardRecipient.year, AwardRecipient.institution, AwardRecipient.notes]

    can_view_details = True
    page_size = 25


# ---------------------------------------------------------------------------
# Donation Methods
# ---------------------------------------------------------------------------

class DonationMethodView(ModelView, model=DonationMethod):
    name = "Donation Method"
    name_plural = "Donation Methods"
    icon = "fa-solid fa-building-columns"
    category = "Donation"

    column_list = [DonationMethod.id, DonationMethod.provider_name, DonationMethod.account_name, DonationMethod.account_number, DonationMethod.method_type, DonationMethod.is_active]
    column_searchable_list = [DonationMethod.provider_name, DonationMethod.account_number]
    column_sortable_list = [DonationMethod.provider_name, DonationMethod.method_type, DonationMethod.display_order, DonationMethod.is_active]
    column_filters = [AllUniqueStringValuesFilter(DonationMethod.method_type), BooleanFilter(DonationMethod.is_active)]
    column_details_list = [DonationMethod.id, DonationMethod.provider_name, DonationMethod.account_name, DonationMethod.account_number, DonationMethod.currency, DonationMethod.method_type, DonationMethod.logo_url, DonationMethod.display_order, DonationMethod.is_active]
    form_columns = [DonationMethod.provider_name, DonationMethod.account_name, DonationMethod.account_number, DonationMethod.currency, DonationMethod.method_type, DonationMethod.display_order, DonationMethod.is_active]

    can_view_details = True
    page_size = 20

    async def scaffold_form(self, rules: List[str] | None = None) -> Type[Form]:
        form_class = await super().scaffold_form(rules)
        form_class.logo = FileField("Logo", validators=[Optional()])
        form_class.method_type = SelectField(
            "Method Type",
            choices=[("bank", "Bank Account"), ("wallet", "Mobile Wallet")],
            default="bank"
        )
        return form_class

    async def on_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        url = await _save_upload(request, "logo", subfolder="images")
        if url:
            model.logo_url = url


# ---------------------------------------------------------------------------
# Submissions
# ---------------------------------------------------------------------------

class ContactSubmissionView(ModelView, model=ContactSubmission):
    name = "Contact Message"
    name_plural = "Contact Messages"
    icon = "fa-solid fa-envelope"
    category = "Submissions"

    column_list = [ContactSubmission.id, ContactSubmission.full_name, ContactSubmission.email, ContactSubmission.subject, ContactSubmission.is_read, ContactSubmission.created_at]
    column_searchable_list = [ContactSubmission.full_name, ContactSubmission.email, ContactSubmission.subject]
    column_sortable_list = [ContactSubmission.created_at, ContactSubmission.is_read, ContactSubmission.full_name]
    column_default_sort = [(ContactSubmission.created_at, True)]
    column_filters = [BooleanFilter(ContactSubmission.is_read)]
    column_details_list = [ContactSubmission.id, ContactSubmission.full_name, ContactSubmission.email, ContactSubmission.subject, ContactSubmission.message, ContactSubmission.is_read, ContactSubmission.created_at]
    form_columns = [ContactSubmission.is_read]

    can_create = False
    can_view_details = True
    page_size = 30


class InterestSubmissionView(ModelView, model=InterestSubmission):
    name = "Summer School Interest"
    name_plural = "Summer School Interests"
    icon = "fa-solid fa-graduation-cap"
    category = "Submissions"

    column_list = [InterestSubmission.id, InterestSubmission.full_name, InterestSubmission.email, InterestSubmission.education_level, InterestSubmission.is_read, InterestSubmission.created_at]
    column_searchable_list = [InterestSubmission.full_name, InterestSubmission.email]
    column_sortable_list = [InterestSubmission.created_at, InterestSubmission.is_read, InterestSubmission.education_level, InterestSubmission.full_name]
    column_default_sort = [(InterestSubmission.created_at, True)]
    column_filters = [BooleanFilter(InterestSubmission.is_read), AllUniqueStringValuesFilter(InterestSubmission.education_level)]
    column_details_list = [InterestSubmission.id, InterestSubmission.full_name, InterestSubmission.email, InterestSubmission.education_level, InterestSubmission.motivation, InterestSubmission.is_read, InterestSubmission.created_at]
    form_columns = [InterestSubmission.is_read]

    can_create = False
    can_view_details = True
    page_size = 30
