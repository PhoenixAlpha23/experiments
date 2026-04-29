# server.py
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from pathlib import Path
import shutil
import logging
import secrets
from typing import List 
import constants
app = FastAPI(title="File Share API")
security = HTTPBasic()

STORAGE_DIR = Path("D:/Code/sharedd")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------
# Logging
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("file_api")

# ------------------------
# Models (Pydantic v2)
# ------------------------
class UploadResponse(BaseModel):
    status: str
    file: str


class FileListResponse(BaseModel):
    files: List[str]


# ------------------------
# Auth
# ------------------------
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if not (
        secrets.compare_digest(credentials.username, constants.username) and
        secrets.compare_digest(credentials.password, constants.password)
    ):
        logger.warning("Unauthorized access")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return credentials.username


# ------------------------
# Utils
# ------------------------
def safe_filename(filename: str) -> str:
    return Path(filename).name  # prevents path traversal


def get_file_path(filename: str) -> Path:
    return STORAGE_DIR / safe_filename(filename)


# ------------------------
# Routes
# ------------------------
@app.post("/upload", response_model=UploadResponse)
async def upload(
    file: UploadFile = File(...),
    user: str = Depends(authenticate)
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    path = get_file_path(file.filename)

    if path.exists():
        raise HTTPException(status_code=409, detail="File already exists")

    try:
        with path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"{user} uploaded {file.filename}")
        return UploadResponse(status="uploaded", file=file.filename)

    except Exception:
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail="Upload failed")


@app.get("/files", response_model=FileListResponse)
def list_files(user: str = Depends(authenticate)):
    try:
        files = [f.name for f in STORAGE_DIR.iterdir() if f.is_file()]
        return FileListResponse(files=files)

    except Exception:
        logger.exception("List files failed")
        raise HTTPException(status_code=500, detail="Could not list files")


@app.get("/download/{filename}")
def download(filename: str, user: str = Depends(authenticate)):
    path = get_file_path(filename)

    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    logger.info(f"{user} downloaded {filename}")
    return FileResponse(path, filename=filename)