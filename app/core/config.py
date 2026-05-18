from pathlib import Path

# ── Base storage ────────────────────────────────────────────────────────────
STORAGE_DIR = Path("D:/Code/sharedd")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# ── Typed sub-directories (created on startup) ───────────────────────────────
PAPERS_DIR = STORAGE_DIR / "papers"
URLS_DIR   = STORAGE_DIR / "urls"
IMAGES_DIR = STORAGE_DIR / "images"
MISC_DIR   = STORAGE_DIR / "misc"

for _dir in (PAPERS_DIR, URLS_DIR, IMAGES_DIR, MISC_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# ── ChromaDB persist location ────────────────────────────────────────────────
CHROMA_DIR = STORAGE_DIR / "chroma_store"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

# ── Chunking config (swap these out freely later) ───────────────────────────
CHUNK_SIZE    = 500   # tokens per chunk
CHUNK_OVERLAP = 50    # overlap between chunks

# ── Embedding model (must be 3.8 compatible, ~80MB) ─────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ── ChromaDB collection name ─────────────────────────────────────────────────
COLLECTION_NAME = "second_brain"