import os
import logging
from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx
from .text_parser import extract_text_from_txt

logger = logging.getLogger(__name__)

PARSER_MAP = {
    ".pdf":  extract_text_from_pdf,
    ".docx": extract_text_from_docx,
    ".txt":  extract_text_from_txt,
}


def parse_document(file_path: str) -> str:
    """
    detect file type and extract text using the correct parser.

    Args:
        file_path (str): Path to the document file.

    Returns:
        str: Extracted text content from the document.

    Raises:
        ValueError: If the file type is not supported.
        RuntimeError: If parsing fails.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext not in PARSER_MAP:
        supported = ", ".join(PARSER_MAP.keys())
        logger.error(f"Unsupported file type: '{ext}' for file: {file_path}")
        raise ValueError(
            f"Unsupported file type: '{ext}'. Supported types are: {supported}"
        )

    parser_fn = PARSER_MAP[ext]
    logger.info(f"Parsing file: {file_path} using parser for '{ext}'")

    text = parser_fn(file_path)

    if not text:
        logger.warning(f"Empty content extracted from file: {file_path}")

    return text