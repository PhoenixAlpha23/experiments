# Stash

Initially as a way to move files from my phone to my old laptop without touching Google Drive.
Grew into a personal knowledge base I actually use.

Problem statement: To store everything I come across that's worth keeping — papers, articles, docs, images — into  a _Stash_. Store it, index it, and find it later. Because like many , even I "save for later" but never be able to actually use it later.

Still Personal. Still running on the same old laptop. Just doing a lot more now.

---

## What it does now

- 📤 Upload files over HTTP — one or many at a time
- 📥 Download files anytime
- 📄 List stored files, sorted by type
- 🌐 Paste a URL — it scrapes the article, strips the noise, indexes the content
- 🔍 Search across everything you've saved — returns ranked results with source and snippet
- 🧠 Chunks and indexes documents automatically on upload

---

## Why I built this

- Reuse old hardware instead of letting it sit idle
- Avoid uploading personal files to third-party cloud services
- Have a controlled environment to **learn FastAPI + backend design**

---

## Stack

| Layer | Tech |
|---|---|
| API | FastAPI |
| UI | Jinja2 + vanilla JS |
| PDF extraction | PyMuPDF |
| Web scraping | requests + readability-lxml + BeautifulSoup4 |
| Index store | JSON-based (ChromaDB + semantic search coming) |
| Chunking | Custom sliding window, plug-and-play |
| Runtime | Python 3.8 |

---

## Hardware this runs on

Old i5 laptop. 8GB RAM. 250GB HDD. Windows 7. Python 3.8.
Every decision in this codebase exists because of at least one of those constraints.

---

## Running it

```bash
# activate your venv first
envvv\Scripts\activate

# start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
---

## Project structure

```
stash/
├── app/
│   ├── api/routes.py          # all endpoints
│   ├── brain/
│   │   ├── chroma.py          # index store
│   │   ├── chunker.py         # text chunker
│   │   ├── extractor.py       # pdf / url / image extraction
│   │   └── ingestor.py        # extract → chunk → store
│   ├── core/
│   │   ├── auth.py            # basic auth
│   │   └── config.py          # all paths and constants
│   ├── models/schemas.py
│   ├── services/storage.py    # file save + routing by type
│   └── templates/index.html   # UI
├── main.py
├── required.txt
└── README.md
```

---

## Roadmap

- [ ] Semantic search (sentence-transformers + ChromaDB) — blocked on PyTorch/Win7
- [ ] Local LLM inference — Mistral 7B Q4 via llama-cpp-python
- [ ] Full RAG pipeline — natural language answers from saved documents
- [ ] Auto-tagging via KeyBERT
- [ ] CV pipeline for image classification
- [ ] MLflow for experiment tracking

---

## Notes

Personal project. Built for personal use.
No tests. No CI. The machine it runs on is _a fragile_.

*Built for me. But if it's useful to you too, cool.*
