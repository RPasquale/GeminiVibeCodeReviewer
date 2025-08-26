"""
Main FastAPI application with DSPy integration for advanced LLM functionality.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import logging
from loguru import logger

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router
from app.services.dspy_service import DSPyService
from app.services.optimization_service import OptimizationService
from app.services.training_service import TrainingService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger.add("logs/app.log", rotation="500 MB", retention="10 days")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Vibe Code Reviewer Backend...")
    
    # Initialize database
    await init_db()
    
    # Initialize DSPy services
    app.state.dspy_service = DSPyService()
    app.state.optimization_service = OptimizationService()
    app.state.training_service = TrainingService()
    
    logger.info("Backend startup complete!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down backend...")

# Create FastAPI app
app = FastAPI(
    title="Vibe Code Reviewer API",
    description="Advanced code review system powered by DSPy framework",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "vibe-code-reviewer"}

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Vibe Code Reviewer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
