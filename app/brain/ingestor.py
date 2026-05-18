"""
Auto-tagging removed for now (keybert brings in heavy deps).

"""

import uuid
import logging
from typing import List, Optional

from app.brain.chroma import get_collection
from app.brain.extractor import extract
from app.brain.chunker import chunk_text

logger = logging.getLogger("ingestor")


def _auto_tag(text: str) -> List[str]:
    """
    Plug keybert:
        pip install keybert==0.7.0
        from keybert import KeyBERT
        kw_model = KeyBERT(model="all-MiniLM-L6-v2")
        return [kw[0] for kw in kw_model.extract_keywords(text[:5000], top_n=5)]
    """
    return []

def ingest(input_data: str, file_type: str) -> dict:
    """
    Full ingestion pipeline for a single document.

    Args:
        input_data: file path (str) for pdf/image, raw URL for url
        file_type:  "pdf" | "url" | "image"

    Returns:
        {title, file_type, tags, chunks_stored}
    """
    collection = get_collection()

    # 1. Extract
    logger.info(f"Extracting [{file_type}]: {input_data}")
    extracted = extract(input_data, file_type)

    text  = extracted.get("text", "")
    title = extracted["title"]
    tags  = _auto_tag(text) if text else []

    # 2. Chunk
    chunks = chunk_text(text)
    if not chunks:
        chunks = [f"[No text content — {file_type}: {title}]"]

    logger.info(f"Chunked into {len(chunks)} chunks")

    # 3. Build metadata (JSON store requires str / int / float values only)
    base_metadata = {
        "type":          extracted["type"],
        "title":         title,
        "file_path":     extracted.get("file_path", ""),
        "source_url":    extracted.get("source_url", ""),
        "source_domain": extracted.get("source_domain", ""),
        "author":        extracted.get("author", "unknown"),
        "pages":         extracted.get("pages", 0),
        "tags":          ", ".join(tags),
        "date_saved":    extracted["date_saved"],
        "summary":       "",
    }

    # 4. Store each chunk
    ids       = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        chunk_meta = {**base_metadata, "chunk_index": i}
        chunk_id   = f"{uuid.uuid4().hex}_{i}"
        ids.append(chunk_id)
        documents.append(chunk)
        metadatas.append(chunk_meta)

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    logger.info(f"Stored {len(chunks)} chunks for '{title}'")

    return {
        "title":         title,
        "file_type":     file_type,
        "tags":          tags,
        "chunks_stored": len(chunks),
    }


# ── Recall ────────────────────────────────────────────────────────────────────
def recall(
    query:       str,
    n_results:   int = 5,
    filter_type: Optional[str] = None,
) -> List[dict]:
    """
    Keyword search over indexed documents.
    Swap for semantic search when embeddings are added.
    """
    collection = get_collection()

    where = {"type": filter_type} if filter_type else None

    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    output = []
    docs      = results["documents"][0]
    metas     = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(docs, metas, distances):
        output.append({
            "title":      meta.get("title", "Untitled"),
            "file_type":  meta.get("type", "unknown"),
            "source":     meta.get("source_url") or meta.get("file_path", ""),
            "snippet":    doc[:400],
            "tags":       meta.get("tags", ""),
            "date_saved": meta.get("date_saved", ""),
            "score":      round(1 - dist, 4),
        })

    return output