from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..security import get_current_admin


router = APIRouter()


# =====================================================
# PUBLIC — GET ALL PRODUCTS
# =====================================================

@router.get("/")
def get_products(
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Product)
        .order_by(models.Product.id.desc())
        .all()
    )


# =====================================================
# ADMIN ONLY — CREATE PRODUCT
# =====================================================

@router.post("/")
def create_product(
    product: dict,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    new_product = models.Product(
        name=product.get("name"),
        tagline=product.get("tagline"),
        description=product.get("description"),
        image=product.get("image"),
        button=product.get("button"),
        features=product.get("features"),
        is_active=product.get("is_active", True),
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# =====================================================
# ADMIN ONLY — UPDATE PRODUCT
# =====================================================

@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: dict,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    existing_product = (
        db.query(models.Product)
        .filter(
            models.Product.id == product_id
        )
        .first()
    )

    if not existing_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    existing_product.name = product.get(
        "name",
        existing_product.name,
    )

    existing_product.tagline = product.get(
        "tagline",
        existing_product.tagline,
    )

    existing_product.description = product.get(
        "description",
        existing_product.description,
    )

    existing_product.image = product.get(
        "image",
        existing_product.image,
    )

    existing_product.button = product.get(
        "button",
        existing_product.button,
    )

    existing_product.features = product.get(
        "features",
        existing_product.features,
    )

    existing_product.is_active = product.get(
        "is_active",
        existing_product.is_active,
    )

    db.commit()
    db.refresh(existing_product)

    return existing_product


# =====================================================
# ADMIN ONLY — DELETE PRODUCT
# =====================================================

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    product = (
        db.query(models.Product)
        .filter(
            models.Product.id == product_id
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully",
    }