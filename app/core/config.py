from pathlib import Path

STORAGE_DIR = Path("D:/Code/sharedd")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

PAPERS_DIR = STORAGE_DIR / "papers"
URLS_DIR   = STORAGE_DIR / "urls"
IMAGES_DIR = STORAGE_DIR / "images"
MISC_DIR   = STORAGE_DIR / "misc"

for _dir in (PAPERS_DIR, URLS_DIR, IMAGES_DIR, MISC_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

CHROMA_DIR = STORAGE_DIR / "chroma_store"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

CHUNK_SIZE    = 500   
CHUNK_OVERLAP = 50    


EMBEDDING_MODEL = "all-MiniLM-L6-v2"

COLLECTION_NAME = "second_brain"