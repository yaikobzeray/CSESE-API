from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentAdmin, DbSession
from app.crud import job as crud
from app.models.job import JobStatus
from app.schemas.job import JobCreate, JobOut, JobUpdate

router = APIRouter(tags=["Jobs & Fellowships"])


@router.get("/", response_model=list[JobOut])
def list_jobs(
    db: DbSession,
    job_status: Annotated[JobStatus | None, Query(alias="status")] = None,
    fellowships_only: Annotated[bool | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 20,
):
    return crud.get_all_jobs(
        db,
        published_only=True,
        status=job_status,
        fellowships_only=fellowships_only,
        skip=skip,
        limit=limit,
    )


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: DbSession):
    item = crud.get_job(db, job_id)
    if not item:
        raise HTTPException(status_code=404, detail="Job not found")
    return item


@router.post("/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(data: JobCreate, db: DbSession, _: CurrentAdmin):
    return crud.create_job(db, data)


@router.patch("/{job_id}", response_model=JobOut)
def update_job(job_id: int, data: JobUpdate, db: DbSession, _: CurrentAdmin):
    item = crud.get_job(db, job_id)
    if not item:
        raise HTTPException(status_code=404, detail="Job not found")
    return crud.update_job(db, item, data)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: DbSession, _: CurrentAdmin):
    item = crud.get_job(db, job_id)
    if not item:
        raise HTTPException(status_code=404, detail="Job not found")
    crud.delete_job(db, item)
