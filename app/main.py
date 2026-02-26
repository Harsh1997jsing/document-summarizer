import logging
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.config import Config
from app.api import register_routes


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured app instance.
    """
    app = FastAPI(
        title=Config.APP_TITLE,
        description=Config.APP_DESCRIPTION,
        version=Config.APP_VERSION,
        docs_url="/docs",  
        redoc_url="/redoc"     
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register all API routes
    register_routes(app)


    @app.get("/", tags=["Health"])
    def health():
        return {
            "status": "ok",
            "message": "Document Summarizer API is running.",
            "docs": "/docs",
            "routes": {
                "drive_connect":  "GET  /drive/connect",
                "drive_files":    "GET  /drive/files?folder_id=<id>",
                "summarize":      "POST /summarize",
                "summarize_ping": "GET  /summarize/status"
            }
        }
    
    @app.get("/ui", response_class=HTMLResponse, tags=["UI"])
    def ui_home(request: Request):
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": None,
                "error": None
            }
        )


    @app.on_event("startup")
    async def startup():
        logger.info(f"Document Summarizer API started.")


    @app.on_event("shutdown")
    async def shutdown():
        logger.info("Document Summarizer API shutting down.")

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )