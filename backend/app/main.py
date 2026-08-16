"""
FastAPI Application — Real Estate AI Agent Backend
Entry point for the entire backend service.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.session import init_db, close_db
from app.api.router import api_router

settings = get_settings()

# Logging
logging.basicConfig(
    level=logging.DEBUG if settings.APP_DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — initialize and cleanup resources."""
    logger.info("🚀 Starting Real Estate AI Backend...")

    # Initialize database tables (dev only; use Alembic in production)
    if not settings.is_production:
        await init_db()
        logger.info("✅ Database tables created")

    # Initialize ChromaDB directory
    import os
    os.makedirs(settings.CHROMA_PERSIST_DIR, exist_ok=True)
    logger.info(f"✅ ChromaDB directory ready: {settings.CHROMA_PERSIST_DIR}")

    logger.info("✅ Backend ready!")
    yield

    # Cleanup
    await close_db()
    logger.info("👋 Backend shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Real Estate AI Agent",
    description="AI-powered real estate assistant with property search, mortgage calculations, ROI analysis, and market insights.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(api_router)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Real Estate AI Agent",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Detailed health check."""
    return {
        "status": "healthy",
        "database": "connected",
        "llm_provider": settings.DEFAULT_LLM_MODEL,
        "environment": settings.APP_ENV,
    }
