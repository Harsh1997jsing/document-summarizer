import pymupdf 
import logging

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file .

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from all pages.
    """
    text = ""

    try:
        doc = pymupdf.open(file_path)
        logger.info(f"Opened PDF: {file_path} | Pages: {len(doc)}")

        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text("text")
            if page_text.strip():
                text += f"\n--- Page {page_num} ---\n"
                text += page_text

        doc.close()

        if not text.strip():
            logger.warning(f"No text extracted from PDF: {file_path}")
            return ""

        logger.info(f"Successfully extracted text from PDF: {file_path}")
        return text.strip()

    except Exception as e:
        logger.error(f"Error extracting text from PDF '{file_path}': {e}")
        raise RuntimeError(f"Failed to parse PDF: {file_path}") from e