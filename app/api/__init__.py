from fastapi import FastAPI
from app.api.drive_routes import drive_router
from app.api.summarize_routes import summarize_router


def register_routes(app: FastAPI):
    """
    Register all API routers with the FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(drive_router)
    app.include_router(summarize_router)