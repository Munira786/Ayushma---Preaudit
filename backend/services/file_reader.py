"""
Safely read uploaded TXT and PDF files. Always return readable text (str).
Ignore image content for MVP.
"""
import io
from pathlib import Path

# PDF text extraction (no images)
try:
    import pdfplumber
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    pdfplumber = None


def read_file(content: bytes, filename: str) -> str:
    """
    Read file content and return text as string.
    - TXT: decode as UTF-8 (fallback replace errors).
    - PDF: extract text via pdfplumber; ignore images.
    - Always returns str; never returns bytes. No silent failures.
    """
    if not content:
        print(f"[file_reader] Empty content for {filename}")
        return ""

    name_lower = (filename or "").lower()
    is_pdf = name_lower.endswith(".pdf")

    if is_pdf:
        return _read_pdf(content, filename)
    return _read_txt(content, filename)


def _read_txt(content: bytes, filename: str) -> str:
    """Decode bytes to string. Prefer UTF-8; replace bad chars to avoid bytes issues."""
    try:
        text = content.decode("utf-8")
        print(f"[file_reader] Read TXT {filename} (utf-8), len={len(text)}")
        return text
    except UnicodeDecodeError as e:
        print(f"[file_reader] UTF-8 decode failed for {filename}: {e}; trying latin-1")
        text = content.decode("latin-1", errors="replace")
        return text


def _read_pdf(content: bytes, filename: str) -> str:
    """Extract text from PDF pages. No image/OCR for MVP."""
    if not HAS_PDF:
        print("[file_reader] pdfplumber not installed; cannot read PDF")
        return ""

    try:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            parts = []
            for i, page in enumerate(pdf.pages):
                t = page.extract_text()
                if t:
                    parts.append(t)
            text = "\n".join(parts) if parts else ""
            print(f"[file_reader] Read PDF {filename}, pages={len(pdf.pages)}, text_len={len(text)}")
            return text
    except Exception as e:
        print(f"[file_reader] PDF read failed for {filename}: {e}")
        raise
