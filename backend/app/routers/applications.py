from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid

from ..database import get_db
from .. import models, schemas
from ..security import get_current_admin


router = APIRouter()


UPLOAD_DIR = Path("uploads/applications")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}


# =========================================================
# PUBLIC — SUBMIT JOB APPLICATION
# =========================================================

@router.post(
    "/",
    response_model=schemas.ApplicationResponse,
)
async def create_application(
    job_id: int = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    cover_letter: str = Form(""),
    resume: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    # Check that the job exists
    job = (
        db.query(models.Job)
        .filter(models.Job.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    resume_path = None

    # =====================================================
    # HANDLE RESUME UPLOAD
    # =====================================================

    if resume:
        extension = Path(
            resume.filename
        ).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Resume must be PDF, PNG, JPG, or JPEG.",
            )

        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Generate unique filename
        filename = (
            f"{uuid.uuid4().hex}{extension}"
        )

        destination = UPLOAD_DIR / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                resume.file,
                buffer,
            )

        resume_path = (
            f"/uploads/applications/{filename}"
        )

    # =====================================================
    # CREATE APPLICATION
    # =====================================================

    new_application = models.Application(
        job_id=job_id,
        full_name=full_name,
        email=email,
        phone=phone,
        resume=resume_path,
        cover_letter=cover_letter,
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# =========================================================
# ADMIN ONLY — GET ALL APPLICATIONS
# =========================================================

@router.get(
    "/",
    response_model=list[schemas.ApplicationResponse],
)
def get_applications(
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    return (
        db.query(models.Application)
        .order_by(
            models.Application.created_at.desc()
        )
        .all()
    )


# =========================================================
# ADMIN ONLY — GET SINGLE APPLICATION
# =========================================================

@router.get(
    "/{application_id}",
    response_model=schemas.ApplicationResponse,
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    application = (
        db.query(models.Application)
        .filter(
            models.Application.id == application_id
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


# =========================================================
# ADMIN ONLY — DELETE APPLICATION
# =========================================================

@router.delete(
    "/{application_id}"
)
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    application = (
        db.query(models.Application)
        .filter(
            models.Application.id == application_id
        )
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    # =====================================================
    # DELETE UPLOADED RESUME
    # =====================================================

    if application.resume:
        file_path = Path(
            application.resume.lstrip("/")
        )

        if file_path.exists():
            file_path.unlink()

    # =====================================================
    # DELETE DATABASE RECORD
    # =====================================================

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }