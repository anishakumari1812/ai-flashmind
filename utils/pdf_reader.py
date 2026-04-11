"""
utils/pdf_reader.py – PDF text extraction utility for FlashMind AI.
Uses pdfplumber for clean, reliable text extraction.
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
        import pdfplumber

        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text.strip())

        full_text = "\n\n".join(text_parts)

        if not full_text.strip():
            return None

        return full_text

    except ImportError:
        # Fallback: try PyMuPDF (fitz) if pdfplumber not installed
        try:
            import fitz  # PyMuPDF

            text_parts = []
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text_parts.append(page.get_text())
            doc.close()

            full_text = "\n\n".join(text_parts)
            return full_text if full_text.strip() else None

        except ImportError:
            raise RuntimeError(
                "No PDF library found. Install pdfplumber: pip install pdfplumber"
            )

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
