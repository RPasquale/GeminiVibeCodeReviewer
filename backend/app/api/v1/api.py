"""
Main API router for DSPy Code Reviewer.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import code_review, rag, training, optimization, models

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    code_review.router,
    prefix="/code-review",
    tags=["code-review"]
)

api_router.include_router(
    rag.router,
    prefix="/rag",
    tags=["rag"]
)

api_router.include_router(
    training.router,
    prefix="/training",
    tags=["training"]
)

api_router.include_router(
    optimization.router,
    prefix="/optimization",
    tags=["optimization"]
)

api_router.include_router(
    models.router,
    prefix="/models",
    tags=["models"]
)
