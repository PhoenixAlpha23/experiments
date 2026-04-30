from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
import logging

from app.core.auth import authenticate
from app.services.storage import save_file, list_all_files, get_file_path
from app.models.schemas import UploadResponse, FileListResponse

router = APIRouter()
logger = logging.getLogger("file_api")


@router.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...), user: str = Depends(authenticate)):
    try:
        filename = save_file(file)
        logger.info(f"{user} uploaded {filename}")
        return UploadResponse(status="uploaded", file=filename)
    except Exception:
        logger.exception("Upload failed")
        raise


@router.get("/files", response_model=FileListResponse)
def list_files(user: str = Depends(authenticate)):
    try:
        files = list_all_files()
        return FileListResponse(files=files)
    except Exception:
        logger.exception("List failed")
        raise HTTPException(status_code=500, detail="Could not list files")


@router.get("/download/{filename}")
def download(filename: str, user: str = Depends(authenticate)):
    path = get_file_path(filename)

    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    logger.info(f"{user} downloaded {filename}")
    return FileResponse(path, filename=filename)