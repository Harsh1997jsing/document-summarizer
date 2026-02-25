import os
import io
import logging
from typing import List, Dict

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from app.auth.google_auth import get_credentials

logger = logging.getLogger(__name__)


SUPPORTED_MIME_TYPES = {
    "application/pdf": ".pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
    "text/plain": ".txt",
}


class DriveClient:
    """
    Google Drive client.
    Uses credentials from google_auth.py to list and download documents.
    """

    def __init__(self):
        """
        Initialize DriveClient by getting credentials from google_auth
        and building the Drive API service.
        """
        creds = get_credentials()
        self.service = build("drive", "v3", credentials=creds)
        logger.info("Google Drive service initialized.")


    def list_files(self, folder_id: str) -> List[Dict]:
        """
        List all supported files (.pdf, .docx, .txt) inside a Drive folder.

        Args:
            folder_id (str): Google Drive folder ID.

        Returns:
            List[Dict]: List of file metadata dicts (id, name, mimeType, extension).
        """
        mime_query = " or ".join(
            [f"mimeType='{mime}'" for mime in SUPPORTED_MIME_TYPES.keys()]
        )
        query = f"'{folder_id}' in parents and ({mime_query}) and trashed=false"

        files = []
        page_token = None

        try:
            while True:
                response = self.service.files().list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType)",
                    pageToken=page_token
                ).execute()

                for file in response.get("files", []):
                    file["extension"] = SUPPORTED_MIME_TYPES.get(file["mimeType"], "")
                    files.append(file)
                    logger.debug(f"Found: {file['name']} ({file['mimeType']})")

                page_token = response.get("nextPageToken")
                if not page_token:
                    break

            logger.info(f"Total files found in folder '{folder_id}': {len(files)}")
            return files

        except Exception as e:
            logger.error(f"Error listing files: {e}")
            raise RuntimeError(f"Failed to list files from Google Drive: {e}") from e


    def download_file(self, file_id: str, file_name: str,
                      download_dir: str = "downloads") -> str:
        """
        Download a single file from Google Drive.

        Args:
            file_id (str): Google Drive file ID.
            file_name (str): Name to save file as locally.
            download_dir (str): Local folder to save the file.

        Returns:
            str: Local file path of the downloaded file.
        """
        os.makedirs(download_dir, exist_ok=True)
        local_path = os.path.join(download_dir, file_name)

        try:
            request = self.service.files().get_media(fileId=file_id)
            buffer = io.BytesIO()
            downloader = MediaIoBaseDownload(buffer, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()
                if status:
                    logger.debug(f"Downloading '{file_name}': {int(status.progress() * 100)}%")

            with open(local_path, "wb") as f:
                f.write(buffer.getvalue())

            logger.info(f"Downloaded: '{file_name}' -> {local_path}")
            return local_path

        except Exception as e:
            logger.error(f"Error downloading '{file_name}': {e}")
            raise RuntimeError(f"Failed to download file: {e}") from e



    def download_all_files(self, folder_id: str,
                           download_dir: str = "downloads") -> List[Dict]:
        """
        List and download all supported files from a Drive folder.

        Args:
            folder_id (str): Google Drive folder ID.
            download_dir (str): Local directory to save files.

        Returns:
            List[Dict]: File metadata with added 'local_path' key.
        """
        files = self.list_files(folder_id)

        if not files:
            logger.warning(f"No supported files found in folder: {folder_id}")
            return []

        downloaded = []
        for file in files:
            try:
                local_path = self.download_file(
                    file_id=file["id"],
                    file_name=file["name"],
                    download_dir=download_dir
                )
                file["local_path"] = local_path
                downloaded.append(file)
            except RuntimeError as e:
                logger.warning(f"Skipping '{file['name']}': {e}")

        logger.info(f"Downloaded {len(downloaded)}/{len(files)} files.")
        return downloaded