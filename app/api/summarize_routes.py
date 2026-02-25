import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.pipeline import Pipeline
from app.config import Config

logger = logging.getLogger(__name__)

summarize_router = APIRouter(prefix="/summarize", tags=["Summarizer"])

class SummarizeRequest(BaseModel):
    folder_id: Optional[str] = None
    download_dir: Optional[str] = "downloads"

@summarize_router.post("")
def summarize(request: SummarizeRequest):
    """
    Trigger the full summarization pipeline for a Google Drive folder.

    - Fetches all supported files from Google Drive
    - Parses text from each document
    - Summarizes each document using OpenAI GPT
    - Returns structured results
    """
    try:
        folder_id = request.folder_id if request.folder_id else Config.DRIVE_FOLDER_ID
        if not folder_id:
            raise HTTPException(
                status_code=400,
                detail="Folder ID not provided and not set in config."
            )
        logger.info(f"Starting pipeline for folder: {folder_id}")

        pipeline = Pipeline(
            folder_id=folder_id,
            download_dir=request.download_dir
        )
        results = pipeline.run()
        results = pipeline.run()

        global LAST_RESULTS
        LAST_RESULTS = results

        if not results:
            return {
                "status": "success",
                "message": "No supported files found in the specified folder.",
                "total": 0,
                "results": []
            }

        success = [r for r in results if r["status"] == "success"]
        failed  = [r for r in results if r["status"] == "error"]

        logger.info(f"Pipeline done. Success: {len(success)} | Failed: {len(failed)}")

        return {
            "status": "success",
            "folder_id": folder_id,
            "total": len(results),
            "success_count": len(success),
            "failed_count": len(failed),
            "results": results
        }

    except Exception as e:
        logger.error(f"Pipeline error: {e}")
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")


@summarize_router.get("/download/csv")
def download_csv():
    import csv, io
    from fastapi.responses import StreamingResponse

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["File Name", "Status", "Summary"])

    for r in LAST_RESULTS:
        writer.writerow([
            r.get("file_name") or r.get("name"),
            r.get("status"),
            r.get("summary") or r.get("error", "")
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=summaries.csv"},
    )

