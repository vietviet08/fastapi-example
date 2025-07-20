from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.api.v1.router import api_router
from app.db.init_db import init_database
import logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc"
    )
    
    @app.on_event("startup")
    async def startup_event():
        """Initialize database on application startup"""
        init_database()
    
    # Configure CORS
    # Note: When allow_origins=["*"], allow_credentials must be False
    # allow_credentials = not ("*" in settings.allowed_origins)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/")
    def root():
        return {"message": f"Welcome to {settings.app_name}"}
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    return app
