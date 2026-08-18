from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import (
    verify_password,
    create_access_token,
    get_current_admin,
)

router = APIRouter()


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_admin: str = Depends(get_current_admin),
):
    total_jobs = db.query(models.Job).count()
    total_contacts = db.query(models.Contact).count()

    active_jobs = (
        db.query(models.Job)
        .filter(models.Job.is_active == True)
        .count()
    )

    return {
        "jobs": total_jobs,
        "contacts": total_contacts,
        "applications": 0,
        "active_jobs": active_jobs,
    }


@router.post("/login", response_model=schemas.Token)
def login(
    admin: schemas.AdminLogin,
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.Admin)
        .filter(models.Admin.username == admin.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    if not verify_password(
        admin.password,
        user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    token = create_access_token(
        {
            "sub": user.username,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }