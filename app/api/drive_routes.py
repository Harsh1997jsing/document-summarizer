import logging
from fastapi import APIRouter, HTTPException, Query
from app.clients.drive_client import DriveClient

logger = logging.getLogger(__name__)

drive_router = APIRouter(prefix="/drive", tags=["Google Drive"])


@drive_router.get("/connect")
def connect():
    """
    Test Google Drive connection.
    Authenticates using OAuth2 and confirms the connection is working.
    """
    try:
        DriveClient()
        logger.info("Google Drive connected successfully.")
        return {
            "status": "connected",
            "message": "Google Drive connected successfully."
        }

    except FileNotFoundError as e:
        logger.error(f"Credentials file missing: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        logger.error(f"Drive connection failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to Google Drive: {str(e)}"
        )


@drive_router.get("/files")
def list_files(folder_id: str | None = Query(default=None, description="Google Drive Folder ID")):
    """
    List all supported files (.pdf, .docx, .txt) in a Google Drive folder.
    """
    try:
        if not folder_id:
            from app.config import Config
            folder_id = Config.DRIVE_FOLDER_ID

        if not folder_id:
            raise HTTPException(
                status_code=400,
                detail="Folder ID not provided and not set in config."
            )

        client = DriveClient()
        files = client.list_files(folder_id)

        return {
            "status": "success",
            "folder_id": folder_id,
            "total": len(files),
            "files": [
                {
                    "id":        f["id"],
                    "name":      f["name"],
                    "mimeType":  f["mimeType"],
                    "extension": f["extension"]
                }
                for f in files
            ]
        }

    except Exception as e:
        logger.error(f"Error listing Drive files: {e}")
        raise HTTPException(status_code=500, detail=str(e))