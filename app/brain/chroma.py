import json
from pathlib import Path
from app.core.config import CHROMA_DIR

_STORE_PATH = Path(CHROMA_DIR) / "store.json"


# ── Internal helpers ──────────────────────────────────────────────────────────

def _load() -> dict:
    if _STORE_PATH.exists():
        with _STORE_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"documents": [], "metadatas": [], "ids": []}


def _save(store: dict):
    with _STORE_PATH.open("w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)


# ── Fake collection object (mirrors ChromaDB collection interface) ─────────────

class _JSONCollection:

    def count(self) -> int:
        return len(_load()["ids"])

    def add(self, ids: list, documents: list, metadatas: list):
        store = _load()
        store["ids"].extend(ids)
        store["documents"].extend(documents)
        store["metadatas"].extend(metadatas)
        _save(store)

    def query(
        self,
        query_texts: list,
        n_results: int = 5,
        where: dict = None,
        include: list = None,
    ) -> dict:
        """
        Basic keyword search — no embeddings.
        Scores by how many query words appear in the document chunk.
        Good enough for testing retrieval logic end-to-end.
        """
        store    = _load()
        query    = query_texts[0].lower() if query_texts else ""
        keywords = query.split()

        scored = []
        for doc, meta, doc_id in zip(
            store["documents"], store["metadatas"], store["ids"]
        ):
            # apply type filter if present
            if where and meta.get("type") != where.get("type"):
                continue

            # score = number of query keywords found in chunk
            doc_lower = doc.lower()
            score = sum(1 for kw in keywords if kw in doc_lower)
            scored.append((score, doc, meta, doc_id))

        # sort by score descending, take top n
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:n_results]

        return {
            "documents": [[item[1] for item in top]],
            "metadatas": [[item[2] for item in top]],
            "distances": [[1 - (item[0] / max(len(keywords), 1)) for item in top]],
            "ids":       [[item[3] for item in top]],
        }


# ── Singleton ─────────────────────────────────────────────────────────────────

_collection = None


def get_collection() -> _JSONCollection:
    global _collection
    if _collection is None:
        _STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _collection = _JSONCollection()
    return _collection


def collection_stats() -> dict:
    return {
        "collection":   "json_store",
        "total_chunks": get_collection().count(),
    }