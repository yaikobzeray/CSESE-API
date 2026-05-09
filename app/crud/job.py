from sqlalchemy.orm import Session

from app.models.job import Job, JobStatus
from app.schemas.job import JobCreate, JobUpdate


def get_job(db: Session, job_id: int) -> Job | None:
    return db.get(Job, job_id)


def get_all_jobs(
    db: Session,
    *,
    published_only: bool = True,
    status: JobStatus | None = None,
    fellowships_only: bool | None = None,
    skip: int = 0,
    limit: int = 20,
) -> list[Job]:
    q = db.query(Job)
    if published_only:
        q = q.filter(Job.is_published == True)  # noqa: E712
    if status:
        q = q.filter(Job.status == status)
    if fellowships_only is not None:
        q = q.filter(Job.is_fellowship == fellowships_only)
    return q.order_by(Job.created_at.desc()).offset(skip).limit(limit).all()


def create_job(db: Session, data: JobCreate) -> Job:
    job = Job(**data.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_job(db: Session, job: Job, data: JobUpdate) -> Job:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job: Job) -> None:
    db.delete(job)
    db.commit()
