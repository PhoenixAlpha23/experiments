from pathlib import Path
from urllib.parse import urlparse
from datetime import date
from typing import Union


def extract_pdf(filepath: Union[str, Path]) -> dict:
    """
    Extract text and metadata from a PDF file using PyMuPDF.
    """
    try:
        import fitz   # PyMuPDF — pip install pymupdf==1.23.8
    except ImportError:
        raise RuntimeError("PyMuPDF not installed. Run: pip install pymupdf==1.23.8")

    filepath = Path(filepath)
    doc      = fitz.open(str(filepath))
    meta     = doc.metadata or {}

    full_text = ""
    for page in doc:
        full_text += page.get_text()

    title = (meta.get("title") or "").strip() or filepath.stem

    return {
        "type":          "pdf",
        "title":         title,
        "author":        (meta.get("author") or "unknown").strip(),
        "pages":         len(doc),
        "file_path":     str(filepath.resolve()),
        "source_url":    "",
        "source_domain": "",
        "date_saved":    date.today().isoformat(),
        "text":          full_text.strip(),
    }

def extract_url(url: str) -> dict:
    """
    Scrape a URL, strip boilerplate, return clean article text + metadata.
    """
    try:
        import requests
        from readability import Document
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError(
            "Missing packages. Run:\n"
            "pip install requests==2.31.0 readability-lxml==0.8.1 beautifulsoup4==4.12.2"
        )

    headers  = {"User-Agent": "Mozilla/5.0 (compatible; SecondBrain/1.0)"}
    response = requests.get(url, timeout=15, headers=headers)
    response.raise_for_status()

    doc        = Document(response.text)
    soup       = BeautifulSoup(doc.summary(), "html.parser")
    clean_text = soup.get_text(separator=" ", strip=True)
    domain     = urlparse(url).netloc

    return {
        "type":          "url",
        "title":         doc.title().strip() or url,
        "author":        "unknown",
        "pages":         0,
        "file_path":     "",
        "source_url":    url,
        "source_domain": domain,
        "date_saved":    date.today().isoformat(),
        "text":          clean_text.strip(),
    }

def extract_image(filepath: Union[str, Path]) -> dict:
    filepath = Path(filepath)
    return {
        "type":          "image",
        "title":         filepath.stem,
        "author":        "unknown",
        "pages":         0,
        "file_path":     str(filepath.resolve()),
        "source_url":    "",
        "source_domain": "",
        "date_saved":    date.today().isoformat(),
        "text":          "",
    }
def extract(input_data: str, file_type: str) -> dict:
    """
    Route to the correct extractor based on file_type.
    """
    if file_type == "pdf":
        return extract_pdf(input_data)
    if file_type == "url":
        return extract_url(input_data)
    if file_type == "image":
        return extract_image(input_data)
    raise ValueError(f"Unknown file_type: {file_type}")