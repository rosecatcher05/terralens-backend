import json

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..security import get_current_admin


router = APIRouter()


# =====================================================
# PUBLIC — GET WEBSITE SETTINGS
# =====================================================

@router.get(
    "/",
    response_model=schemas.SiteSettingsResponse,
)
def get_settings(
    db: Session = Depends(get_db),
):
    settings = (
        db.query(models.SiteSettings)
        .first()
    )

    if not settings:
        settings = models.SiteSettings()

        db.add(settings)
        db.commit()
        db.refresh(settings)

    # Convert stored JSON text into a Python list
    if settings.about_videos:
        try:
            settings.about_videos = json.loads(
                settings.about_videos
            )
        except (json.JSONDecodeError, TypeError):
            settings.about_videos = []
    else:
        settings.about_videos = []

    return settings


# =====================================================
# ADMIN ONLY — UPDATE WEBSITE SETTINGS
# =====================================================

@router.put(
    "/",
    response_model=schemas.SiteSettingsResponse,
)
def update_settings(
    data: schemas.SiteSettingsUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin),
):
    received = data.model_dump(
        exclude_unset=True
    )

    print(
        "SETTINGS RECEIVED:",
        received,
    )

    # Convert about_videos list → JSON string
    if "about_videos" in received:
        print(
            "ABOUT VIDEOS RECEIVED:",
            received["about_videos"],
        )

        received["about_videos"] = json.dumps(
            received["about_videos"]
        )

    settings = (
        db.query(models.SiteSettings)
        .first()
    )

    if not settings:
        settings = models.SiteSettings()

        db.add(settings)
        db.commit()
        db.refresh(settings)

    # Update supplied settings
    for key, value in received.items():
        setattr(
            settings,
            key,
            value,
        )

    db.commit()
    db.refresh(settings)

    # Convert JSON string → list for API response
    response_data = {
        column.name: getattr(
            settings,
            column.name,
        )
        for column in
        models.SiteSettings.__table__.columns
    }

    if response_data.get("about_videos"):
        try:
            response_data["about_videos"] = json.loads(
                response_data["about_videos"]
            )
        except (json.JSONDecodeError, TypeError):
            response_data["about_videos"] = []
    else:
        response_data["about_videos"] = []

    print(
        "ABOUT VIDEOS SAVED:",
        response_data["about_videos"],
    )

    return response_data