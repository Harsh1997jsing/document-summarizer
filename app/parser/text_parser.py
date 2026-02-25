import logging

logger = logging.getLogger(__name__)

SUPPORTED_ENCODINGS = ["utf-8", "utf-16", "latin-1", "cp1252"]


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text content from a plain TXT file.
    Tries multiple encodings to handle different file formats.

    Args:
        file_path (str): Path to the TXT file.

    Returns:
        str: Extracted text content.
    """
    try:
        for encoding in SUPPORTED_ENCODINGS:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    text = f.read()

                if text.strip():
                    logger.info(f"Successfully read TXT file '{file_path}' with encoding: {encoding}")
                    return text.strip()

            except (UnicodeDecodeError, UnicodeError):
                logger.debug(f"Encoding '{encoding}' failed for file: {file_path}, trying next...")
                continue

        logger.warning(f"No text extracted or unsupported encoding for TXT: {file_path}")
        return ""

    except FileNotFoundError:
        logger.error(f"TXT file not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    except Exception as e:
        logger.error(f"Error reading TXT file '{file_path}': {e}")
        raise RuntimeError(f"Failed to parse TXT: {file_path}") from e