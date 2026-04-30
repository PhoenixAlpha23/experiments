from pathlib import Path
import shutil
from fastapi import UploadFile, HTTPException
from app.core.config import STORAGE_DIR


def safe_filename(filename: str) -> str:
    return Path(filename).name


def get_file_path(filename: str) -> Path:
    return STORAGE_DIR / safe_filename(filename)


def save_file(file: UploadFile):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    path = get_file_path(file.filename)

    if path.exists():
        raise HTTPException(status_code=409, detail="File already exists")

    with path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file.filename


def list_all_files():
    return [f.name for f in STORAGE_DIR.iterdir() if f.is_file()]