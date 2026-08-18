from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
)
from pathlib import Path
import shutil

from ..security import get_current_admin


router = APIRouter()

UPLOAD_DIR = Path("uploads")


# =====================================================
# PUBLIC — LIST MEDIA
# =====================================================

@router.get("/")
def list_media():
    files = []

    if not UPLOAD_DIR.exists():
        return files

    for folder in UPLOAD_DIR.iterdir():
        if folder.is_dir():
            for file in folder.iterdir():
                if file.is_file():
                    files.append({
                        "folder": folder.name,
                        "filename": file.name,
                        "path": f"/uploads/{folder.name}/{file.name}",
                    })

    return files


# =====================================================
# ADMIN ONLY — DELETE MEDIA
# =====================================================

@router.delete("/{folder}/{filename}")
def delete_media(
    folder: str,
    filename: str,
    admin: str = Depends(get_current_admin),
):
    file_path = UPLOAD_DIR / folder / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    file_path.unlink()

    return {
        "message": "Deleted successfully",
    }


# =====================================================
# ADMIN ONLY — UPLOAD MEDIA
# =====================================================

@router.post("/upload/{folder}")
async def upload_file(
    folder: str,
    file: UploadFile = File(...),
    admin: str = Depends(get_current_admin),
):
    folder_path = UPLOAD_DIR / folder

    folder_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination = folder_path / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return {
        "filename": file.filename,
        "path": f"/uploads/{folder}/{file.filename}",
    }