"""
Code review API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List
import time
from loguru import logger

from app.models.code_review import (
    CodeReviewRequest, 
    CodeReviewResponse, 
    BatchCodeReviewRequest, 
    BatchCodeReviewResponse
)
from app.services.dspy_service import DSPyService
from app.core.database import get_db

router = APIRouter()

async def get_dspy_service() -> DSPyService:
    """Dependency to get DSPy service."""
    # This would be injected from the app state
    # For now, we'll create a new instance
    return DSPyService()

@router.post("/review", response_model=CodeReviewResponse)
async def review_code(
    request: CodeReviewRequest,
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Review a single piece of code using DSPy.
    
    This endpoint uses DSPy's advanced LLM capabilities to provide comprehensive code reviews.
    """
    try:
        start_time = time.time()
        
        # Perform code review using DSPy
        response = await dspy_service.review_code(request)
        
        # Add processing time
        response.processing_time = time.time() - start_time
        
        logger.info(f"Code review completed in {response.processing_time:.2f}s")
        
        return response
        
    except Exception as e:
        logger.error(f"Error in code review: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/review/batch", response_model=BatchCodeReviewResponse)
async def review_code_batch(
    request: BatchCodeReviewRequest,
    background_tasks: BackgroundTasks,
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Review multiple files in batch using DSPy.
    
    This endpoint processes multiple files and provides both individual and cross-file analysis.
    """
    try:
        start_time = time.time()
        
        # Process each file
        file_reviews = []
        for file_data in request.files:
            review_request = CodeReviewRequest(
                code=file_data['content'],
                language=request.language,
                context=request.context,
                review_type=request.review_type
            )
            
            review_response = await dspy_service.review_code(review_request)
            file_reviews.append(review_response)
        
        # Calculate overall metrics
        total_score = sum(review.score for review in file_reviews) / len(file_reviews)
        
        # Generate overall summary
        overall_summary = f"Reviewed {len(file_reviews)} files with average score of {total_score:.2f}/10"
        
        # Cross-file analysis (simplified for now)
        cross_file_issues = []
        if request.include_cross_file_analysis and len(file_reviews) > 1:
            # This would implement more sophisticated cross-file analysis
            cross_file_issues = [
                {
                    "type": "consistency",
                    "description": "Check for consistent coding patterns across files",
                    "affected_files": [f"file_{i}" for i in range(len(file_reviews))]
                }
            ]
        
        processing_time = time.time() - start_time
        
        return BatchCodeReviewResponse(
            file_reviews=file_reviews,
            overall_summary=overall_summary,
            cross_file_issues=cross_file_issues,
            total_score=total_score,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Error in batch code review: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize")
async def optimize_code_reviewer(
    training_data: List[dict],
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Optimize the code reviewer using DSPy optimizers.
    
    This endpoint uses DSPy's optimization capabilities to improve the code review model.
    """
    try:
        success = await dspy_service.optimize_code_reviewer(training_data)
        
        if success:
            return {"message": "Code reviewer optimization completed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Optimization failed")
            
    except Exception as e:
        logger.error(f"Error in code reviewer optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_code_review_status(
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Get the status of the code review system.
    
    Returns information about the current model configuration and optimization status.
    """
    try:
        model_info = await dspy_service.get_model_info()
        
        return {
            "status": "operational",
            "model_info": model_info,
            "optimization_status": "available" if hasattr(dspy_service, 'optimized_reviewer') else "not_optimized"
        }
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def submit_review_feedback(
    review_id: str,
    feedback: dict,
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Submit feedback on a code review for continuous improvement.
    
    This feedback can be used to improve the model through DSPy's learning capabilities.
    """
    try:
        # Store feedback for future optimization
        # This would typically be stored in a database
        logger.info(f"Received feedback for review {review_id}: {feedback}")
        
        return {"message": "Feedback submitted successfully"}
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))
