from pathlib import Path
import shutil
from fastapi import UploadFile, HTTPException
from app.core.config import STORAGE_DIR, PAPERS_DIR, URLS_DIR, IMAGES_DIR, MISC_DIR

# ── File type → directory routing ────────────────────────────────────────────
EXTENSION_MAP = {
    # documents / papers
    ".pdf":  PAPERS_DIR,
    ".docx": PAPERS_DIR,
    ".txt":  PAPERS_DIR,
    ".md":   PAPERS_DIR,
    # images
    ".jpg":  IMAGES_DIR,
    ".jpeg": IMAGES_DIR,
    ".png":  IMAGES_DIR,
    ".webp": IMAGES_DIR,
    ".gif":  IMAGES_DIR,
    # url dumps land here (written by scraper, not uploaded directly)
    # everything else
}

def classify_file(filename: str) -> str:
    """Return a type label for a given filename."""
    ext = Path(filename).suffix.lower()
    if ext in (".pdf", ".docx", ".txt", ".md"):
        return "pdf"          # treated as document / paper
    if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
        return "image"
    return "misc"


def get_subdir(filename: str) -> Path:
    """Return the correct sub-directory for a file based on its extension."""
    ext = Path(filename).suffix.lower()
    return EXTENSION_MAP.get(ext, MISC_DIR)


def safe_filename(filename: str) -> str:
    return Path(filename).name


def get_file_path(filename: str) -> Path:
    """
    Search all sub-directories for the file.
    Falls back to STORAGE_DIR root for files uploaded before subdirs existed.
    """
    for directory in (PAPERS_DIR, URLS_DIR, IMAGES_DIR, MISC_DIR, STORAGE_DIR):
        candidate = directory / safe_filename(filename)
        if candidate.exists():
            return candidate
    return STORAGE_DIR / safe_filename(filename)   # will 404 upstream


def save_file(file: UploadFile) -> tuple:
    """
    Save uploaded file to the correct sub-directory.
    Returns (filename, file_type, saved_path).
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename missing")

    name      = safe_filename(file.filename)
    subdir    = get_subdir(name)
    path      = subdir / name
    file_type = classify_file(name)

    if path.exists():
        raise HTTPException(status_code=409, detail="File already exists")

    with path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return name, file_type, path


def list_all_files() -> list:
    """List all files across all sub-directories with their type."""
    result = []
    dirs = {
        "pdf":   PAPERS_DIR,
        "url":   URLS_DIR,
        "image": IMAGES_DIR,
        "misc":  MISC_DIR,
    }
    for file_type, directory in dirs.items():
        for f in directory.iterdir():
            if f.is_file():
                result.append({"name": f.name, "type": file_type})

    # also surface legacy files sitting in root
    for f in STORAGE_DIR.iterdir():
        if f.is_file():
            result.append({"name": f.name, "type": "misc"})

    return result