from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import get_current_admin


router = APIRouter()


# =====================================================
# ADMIN ONLY — CREATE JOB
# =====================================================

@router.post(
    "/",
    response_model=schemas.JobResponse,
)
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    existing_job = (
        db.query(models.Job)
        .filter(
            models.Job.title == job.title,
            models.Job.location == job.location,
        )
        .first()
    )

    if existing_job:
        return existing_job

    new_job = models.Job(
        title=job.title,
        department=job.department,
        location=job.location,
        employment_type=job.employment_type,
        description=job.description,
        requirements=job.requirements,
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# =====================================================
# PUBLIC — GET ALL JOBS
# =====================================================

@router.get(
    "/",
    response_model=list[schemas.JobResponse],
)
def get_jobs(
    db: Session = Depends(get_db),
):
    return db.query(models.Job).all()


# =====================================================
# ADMIN ONLY — UPDATE JOB
# =====================================================

@router.put(
    "/{job_id}",
    response_model=schemas.JobResponse,
)
def update_job(
    job_id: int,
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    existing_job = (
        db.query(models.Job)
        .filter(
            models.Job.id == job_id
        )
        .first()
    )

    if not existing_job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    existing_job.title = job.title
    existing_job.department = job.department
    existing_job.location = job.location
    existing_job.employment_type = job.employment_type
    existing_job.description = job.description
    existing_job.requirements = job.requirements

    db.commit()
    db.refresh(existing_job)

    return existing_job


# =====================================================
# ADMIN ONLY — DELETE JOB
# =====================================================

@router.delete(
    "/{job_id}"
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    job = (
        db.query(models.Job)
        .filter(
            models.Job.id == job_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }