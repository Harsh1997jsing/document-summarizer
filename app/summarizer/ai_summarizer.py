import logging
from app.clients.llm_client import LLMClient

logger = logging.getLogger(__name__)

MAX_CHARS = 12000

SYSTEM_PROMPT = (
    "You are a professional document summarizer. "
    "Your task is to read documents and produce clear, "
    "concise, and accurate summaries in 5 to 10 sentences. "
    "Focus on the main topics, key points, and conclusions."
)


class AISummarizer:
    """
    Summarization service.
    Uses LLMClient to communicate with OpenAI and handles
    all summarization business logic.
    """

    def __init__(self, llm_client: LLMClient = None):
        """
        Initialize AISummarizer with an LLMClient instance.

        Args:
            llm_client (LLMClient): Optional existing LLMClient instance.
                                    Creates a new one if not provided.
        """
        self.llm = llm_client or LLMClient()
        logger.info("AISummarizer initialized.")


    def summarize(self, text: str, file_name: str = "document") -> str:
        """
        Summarize a single document's text.

        Args:
            text (str): Extracted text content from the document.
            file_name (str): Name of the document file (used in prompt).

        Returns:
            str: A 5–10 sentence summary of the document.
        """
        if not text or not text.strip():
            logger.warning(f"Empty text provided for '{file_name}'. Skipping summarization.")
            return "No content available to summarize."

        truncated_text = self._truncate(text)
        user_prompt = self._build_prompt(truncated_text, file_name)

        logger.info(f"Summarizing document: '{file_name}'")
        summary = self.llm.chat(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        logger.info(f"Summarization complete for: '{file_name}'")
        return summary


    def _build_prompt(self, text: str, file_name: str) -> str:
        """
        Build the user prompt for summarization.

        Args:
            text (str): Document text content.
            file_name (str): Name of the file.

        Returns:
            str: Formatted prompt.
        """
        return (
            f"Please summarize the following document titled '{file_name}'.\n"
            f"Provide a clear and concise summary in 5 to 10 sentences, "
            f"covering the main topics, key points, and conclusions.\n\n"
            f"Document Content:\n{text}"
        )

    def _truncate(self, text: str) -> str:
        """
        Truncate text to MAX_CHARS to avoid exceeding token limits.

        Args:
            text (str): Original document text.

        Returns:
            str: Truncated text with a note if truncation occurred.
        """
        if len(text) <= MAX_CHARS:
            return text

        logger.warning(
            f"Text truncated from {len(text)} to {MAX_CHARS} characters."
        )
        return text[:MAX_CHARS] + "\n\n[Note: Document was truncated due to length.]"