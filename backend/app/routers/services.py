from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import get_current_admin


router = APIRouter()


# =====================================================
# PUBLIC — GET ALL SERVICES
# =====================================================

@router.get("/")
def get_services(
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Service)
        .order_by(
            models.Service.created_at.desc()
        )
        .all()
    )


# =====================================================
# PUBLIC — GET SERVICE BY SLUG
# =====================================================

@router.get("/{slug}")
def get_service_by_slug(
    slug: str,
    db: Session = Depends(get_db),
):
    service = (
        db.query(models.Service)
        .filter(
            models.Service.slug == slug
        )
        .first()
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    return service


# =====================================================
# ADMIN ONLY — CREATE SERVICE
# =====================================================

@router.post("/")
def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    existing = (
        db.query(models.Service)
        .filter(
            models.Service.slug == service.slug
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Service slug already exists",
        )

    new_service = models.Service(
        name=service.name,
        slug=service.slug,
        category=service.category,
        description=service.description,
        image=service.image,
        is_active=service.is_active,
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


# =====================================================
# ADMIN ONLY — UPDATE SERVICE
# =====================================================

@router.put("/{service_id}")
def update_service(
    service_id: int,
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    existing = (
        db.query(models.Service)
        .filter(
            models.Service.id == service_id
        )
        .first()
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    existing.name = service.name
    existing.slug = service.slug
    existing.category = service.category
    existing.description = service.description
    existing.image = service.image
    existing.is_active = service.is_active

    db.commit()
    db.refresh(existing)

    return existing


# =====================================================
# ADMIN ONLY — DELETE SERVICE
# =====================================================

@router.delete("/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    existing = (
        db.query(models.Service)
        .filter(
            models.Service.id == service_id
        )
        .first()
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Service not found",
        )

    db.delete(existing)
    db.commit()

    return {
        "message": "Service deleted successfully"
    }