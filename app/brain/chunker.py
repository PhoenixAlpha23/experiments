from typing import List
from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP


# ── Strategy: fixed-size word window ─────────────────────────────────────────
def _word_window(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Splits text into overlapping chunks by word count.

    Args:
        text:       raw extracted text
        chunk_size: max words per chunk  (default: CHUNK_SIZE from config)
        overlap:    words shared between adjacent chunks (default: CHUNK_OVERLAP)

    Returns:
        List of text chunk strings.
    """
    words  = text.split()
    chunks = []
    start  = 0

    while start < len(words):
        end   = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap   # slide forward, keeping overlap

    return [c for c in chunks if c.strip()]   # drop empty chunks


# ── Strategy stub: sentence-aware (plug in later if needed) ──────────────────
def _sentence_window(text: str, chunk_size: int, overlap: int) -> List[str]:
    """
    Placeholder for sentence-aware chunking.
    Useful for conversational text where mid-sentence cuts hurt retrieval.
    Swap chunk_text() below to use this when ready.
    """
    raise NotImplementedError("Sentence-aware chunking not implemented yet.")


# ── Public interface (this is what ingestor.py calls) ─────────────────────────
def chunk_text(
    text:       str,
    chunk_size: int = CHUNK_SIZE,
    overlap:    int = CHUNK_OVERLAP,
) -> List[str]:
    """
    Split text into chunks ready for embedding.
    Change the strategy here without touching anything else.

    Args:
        text:       raw text to chunk
        chunk_size: words per chunk
        overlap:    words of overlap between chunks

    Returns:
        List[str] of chunks.
    """
    if not text or not text.strip():
        return []

    # ← swap strategy here when needed
    return _word_window(text, chunk_size, overlap)