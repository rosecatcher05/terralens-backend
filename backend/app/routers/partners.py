from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import get_current_admin


router = APIRouter()


# =====================================================
# ADMIN ONLY — CREATE PARTNER
# =====================================================

@router.post(
    "/",
    response_model=schemas.PartnerResponse,
)
def create_partner(
    partner: schemas.PartnerCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    new_partner = models.Partner(
        name=partner.name,
        logo=partner.logo,
        type=partner.type,
        is_active=partner.is_active,
    )

    db.add(new_partner)
    db.commit()
    db.refresh(new_partner)

    return new_partner


# =====================================================
# PUBLIC — GET ALL PARTNERS
# =====================================================

@router.get(
    "/",
    response_model=list[schemas.PartnerResponse],
)
def get_partners(
    db: Session = Depends(get_db),
):
    return db.query(models.Partner).all()


# =====================================================
# PUBLIC — GET SINGLE PARTNER
# =====================================================

@router.get(
    "/{partner_id}",
    response_model=schemas.PartnerResponse,
)
def get_partner(
    partner_id: int,
    db: Session = Depends(get_db),
):
    partner = (
        db.query(models.Partner)
        .filter(
            models.Partner.id == partner_id
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner not found",
        )

    return partner


# =====================================================
# ADMIN ONLY — UPDATE PARTNER
# =====================================================

@router.put(
    "/{partner_id}",
    response_model=schemas.PartnerResponse,
)
def update_partner(
    partner_id: int,
    partner: schemas.PartnerCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    existing_partner = (
        db.query(models.Partner)
        .filter(
            models.Partner.id == partner_id
        )
        .first()
    )

    if not existing_partner:
        raise HTTPException(
            status_code=404,
            detail="Partner not found",
        )

    existing_partner.name = partner.name
    existing_partner.logo = partner.logo
    existing_partner.type = partner.type
    existing_partner.is_active = partner.is_active

    db.commit()
    db.refresh(existing_partner)

    return existing_partner


# =====================================================
# ADMIN ONLY — DELETE PARTNER
# =====================================================

@router.delete(
    "/{partner_id}"
)
def delete_partner(
    partner_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    partner = (
        db.query(models.Partner)
        .filter(
            models.Partner.id == partner_id
        )
        .first()
    )

    if not partner:
        raise HTTPException(
            status_code=404,
            detail="Partner not found",
        )

    db.delete(partner)
    db.commit()

    return {
        "message": "Partner deleted successfully"
    }