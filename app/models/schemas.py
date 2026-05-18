from pydantic import BaseModel
from typing import List, Optional

class UploadResponse(BaseModel):
    status: str
    file: str

class FileListResponse(BaseModel):
    files: List[dict]          # now returns {name, type} dicts

# ── Ingest ───────────────────────────────────────────────────────────────────
class IngestResponse(BaseModel):
    status: str
    title: str
    file_type: str             # "pdf" | "url" | "image"
    tags: List[str]
    chunks_stored: int

# ── Recall / Search ──────────────────────────────────────────────────────────
class RecallQuery(BaseModel):
    query: str
    n_results: Optional[int] = 5
    filter_type: Optional[str] = None   # "pdf" | "url" | "image" | None = all

class RecallResult(BaseModel):
    title: str
    file_type: str
    source: str                # file path or URL
    snippet: str               # the matching chunk text
    tags: str
    date_saved: str
    score: Optional[float] = None

class RecallResponse(BaseModel):
    query: str
    results: List[RecallResult]