"""
utils/pdf_reader.py – PDF text extraction utility for FlashMind AI.
Uses pypdf for pure-Python, Render-compatible text extraction.
"""

import io
from typing import Optional


def extract_text_from_pdf(file_bytes: bytes) -> Optional[str]:
    """
    Extract all text from a PDF file given its raw bytes.

    Args:
        file_bytes: Raw bytes of the uploaded PDF file.

    Returns:
        Extracted text as a string, or None if extraction fails.
    """
    try:
        from pypdf import PdfReader

        text_parts = []
        reader = PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text.strip())

        full_text = "\n\n".join(text_parts)

        if not full_text.strip():
            return None

        return full_text

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")


def truncate_text(text: str, max_chars: int = 4000) -> str:
    """
    Truncate text to a maximum character count to avoid token overflows.

    Args:
        text:      The input text.
        max_chars: Maximum number of characters to keep.

    Returns:
        Truncated text with an ellipsis note if trimmed.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[... text truncated for processing ...]"