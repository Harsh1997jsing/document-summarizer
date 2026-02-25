import logging
from typing import List, Dict

from app.clients.drive_client import DriveClient
from app.parser.parser_factory import parse_document
from app.summarizer.ai_summarizer import AISummarizer

logger = logging.getLogger(__name__)


class Pipeline:
    """
    Main orchestration service.
    Connects all modules in sequence:
        Google Drive → Parser → AI Summarizer → Results
    """

    def __init__(self, folder_id: str, download_dir: str = "downloads"):
        """
        Initialize Pipeline with required services.

        Args:
            folder_id (str): Google Drive folder ID to fetch documents from.
            download_dir (str): Local directory to store downloaded files.
        """
        self.folder_id = folder_id
        self.download_dir = download_dir

        # Initialize all services
        self.drive_client = DriveClient()
        self.summarizer = AISummarizer()

        logger.info(f"Pipeline initialized for folder: {folder_id}")

    # ------------------------------------------------------------------
    # Main Run
    # ------------------------------------------------------------------

    def run(self) -> List[Dict]:
        """
        Execute the full pipeline:
            1. Fetch files from Google Drive
            2. Parse text from each file
            3. Summarize each document using AI
            4. Return structured results

        Returns:
            List[Dict]: Each dict contains:
                - file_name  (str): Name of the document
                - summary    (str): AI-generated summary
                - status     (str): 'success' or 'error'
                - error      (str): Error message if status is 'error'
        """
        logger.info("Pipeline started.")
        results = []

        # ---- Step 1: Fetch files from Google Drive ----
        logger.info(f"Step 1: Fetching files from Drive folder: {self.folder_id}")
        files = self._fetch_files()

        if not files:
            logger.warning("No files found in the Drive folder. Pipeline stopped.")
            return []

        logger.info(f"Fetched {len(files)} files from Drive.")

   
        for file in files:
            file_name = file.get("name", "unknown")
            local_path = file.get("local_path", "")
            result = self._process_file(file_name, local_path)
            results.append(result)

        # ---- Summary Log ----
        success = sum(1 for r in results if r["status"] == "success")
        failed  = sum(1 for r in results if r["status"] == "error")
        logger.info(f"Pipeline complete. Success: {success} | Failed: {failed}")

        return results


    def _fetch_files(self) -> List[Dict]:
        """
        Download all supported files from the configured Drive folder.

        Returns:
            List[Dict]: File metadata with 'local_path' included.
        """
        try:
            files = self.drive_client.download_all_files(
                folder_id=self.folder_id,
                download_dir=self.download_dir
            )
            return files
        except Exception as e:
            logger.error(f"Failed to fetch files from Drive: {e}")
            raise RuntimeError(f"Drive fetch error: {e}") from e



    def _parse_file(self, file_name: str, local_path: str) -> str:
        """
        Extract text from a downloaded document.

        Args:
            file_name (str): Name of the file.
            local_path (str): Local path to the file.

        Returns:
            str: Extracted text content.
        """
        logger.info(f"Step 2: Parsing '{file_name}'")
        text = parse_document(local_path)

        if not text or not text.strip():
            logger.warning(f"No text extracted from '{file_name}'.")
            return ""

        logger.info(f"Parsed '{file_name}' — {len(text)} characters extracted.")
        return text



    def _summarize_file(self, file_name: str, text: str) -> str:
        """
        Summarize extracted text using AI.

        Args:
            file_name (str): Name of the document.
            text (str): Extracted text content.

        Returns:
            str: AI-generated summary.
        """
        logger.info(f"Step 3: Summarizing '{file_name}'")
        summary = self.summarizer.summarize(text=text, file_name=file_name)
        logger.info(f"Summarized '{file_name}' successfully.")
        return summary

    # ------------------------------------------------------------------
    # Process Single File (Step 2 + 3 combined)
    # ------------------------------------------------------------------

    def _process_file(self, file_name: str, local_path: str) -> Dict:
        """
        Parse and summarize a single file, handling errors gracefully.

        Args:
            file_name (str): Name of the file.
            local_path (str): Local path to the downloaded file.

        Returns:
            Dict: Result with keys: file_name, summary, status, error (if any).
        """
        try:
            # Step 2: Parse
            text = self._parse_file(file_name, local_path)

            if not text:
                return {
                    "file_name": file_name,
                    "summary": "Could not extract any text from this document.",
                    "status": "error",
                    "error": "Empty content after parsing."
                }

            # Step 3: Summarize
            summary = self._summarize_file(file_name, text)

            return {
                "file_name": file_name,
                "summary": summary,
                "status": "success",
                "error": None
            }

        except Exception as e:
            logger.error(f"Error processing '{file_name}': {e}")
            return {
                "file_name": file_name,
                "summary": f"Processing failed: {str(e)}",
                "status": "error",
                "error": str(e)
            }