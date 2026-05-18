from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import logging

from app.core.auth       import authenticate
from app.services.storage import save_file, list_all_files, get_file_path, classify_file
from app.models.schemas  import UploadResponse, FileListResponse, IngestResponse, RecallQuery, RecallResponse
from app.brain.ingestor  import ingest, recall
from app.brain.chroma    import collection_stats

router = APIRouter()
logger = logging.getLogger("routes")


# ── Existing: upload ──────────────────────────────────────────────────────────
@router.post("/upload", response_model=UploadResponse)
async def upload(
    file:             UploadFile = File(...),
    user:             str        = Depends(authenticate),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    try:
        filename, file_type, saved_path = save_file(file)
        logger.info(f"{user} uploaded {filename} [{file_type}]")

        # kick off indexing in the background so upload returns immediately
        background_tasks.add_task(_index_file, str(saved_path), file_type, filename)

        return UploadResponse(status="uploaded", file=filename)
    except HTTPException:
        raise
    except Exception:
        logger.exception("Upload failed")
        raise HTTPException(status_code=500, detail="Upload failed")


def _index_file(file_path: str, file_type: str, filename: str):
    """Background task — runs after upload returns."""
    try:
        result = ingest(file_path, file_type)
        logger.info(f"Indexed '{result['title']}' — {result['chunks_stored']} chunks")
    except Exception as e:
        logger.error(f"Indexing failed for {filename}: {e}")


# ── Existing: list files ──────────────────────────────────────────────────────
@router.get("/files", response_model=FileListResponse)
def list_files(user: str = Depends(authenticate)):
    try:
        files = list_all_files()
        return FileListResponse(files=files)
    except Exception:
        logger.exception("List failed")
        raise HTTPException(status_code=500, detail="Could not list files")


# ── Existing: download ────────────────────────────────────────────────────────
@router.get("/download/{filename}")
def download(filename: str, user: str = Depends(authenticate)):
    path = get_file_path(filename)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    logger.info(f"{user} downloaded {filename}")
    return FileResponse(path, filename=filename)


# ── New: ingest a URL manually ────────────────────────────────────────────────
@router.post("/ingest/url", response_model=IngestResponse)
async def ingest_url(payload: dict, user: str = Depends(authenticate)):
    """
    Ingest a URL directly — scrapes, indexes, stores.
    Body: { "url": "https://..." }
    """
    url = payload.get("url", "").strip()
    if not url or not url.startswith("http"):
        raise HTTPException(status_code=400, detail="Valid URL required")
    try:
        result = ingest(url, "url")
        return IngestResponse(status="indexed", **result)
    except Exception as e:
        logger.exception("URL ingest failed")
        raise HTTPException(status_code=500, detail=str(e))


# ── New: recall / semantic search ─────────────────────────────────────────────
@router.post("/recall", response_model=RecallResponse)
def recall_query(payload: RecallQuery, user: str = Depends(authenticate)):
    """
    Semantic search over everything indexed in ChromaDB.
    Body: { "query": "...", "n_results": 5, "filter_type": "pdf" | "url" | null }
    """
    try:
        results = recall(
            query=payload.query,
            n_results=payload.n_results,
            filter_type=payload.filter_type,
        )
        return RecallResponse(query=payload.query, results=results)
    except Exception as e:
        logger.exception("Recall failed")
        raise HTTPException(status_code=500, detail=str(e))


# ── New: ChromaDB health check ────────────────────────────────────────────────
@router.get("/brain/stats")
def brain_stats(user: str = Depends(authenticate)):
    """Returns how many chunks are stored in ChromaDB."""
    return collection_stats()