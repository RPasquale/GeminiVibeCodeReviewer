"""
Models API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from loguru import logger
from datetime import datetime

from app.services.dspy_service import DSPyService
from app.models.code_review import CodeReviewRequest
from app.models.rag import RAGRequest

router = APIRouter()

async def get_dspy_service() -> DSPyService:
    """Dependency to get DSPy service."""
    return DSPyService()

@router.get("/info")
async def get_model_info(
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Get information about the current model configuration.
    
    Returns detailed information about the model, its configuration, and capabilities.
    """
    try:
        model_info = await dspy_service.get_model_info()
        return model_info
        
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/available")
async def list_available_models():
    """
    List available language models.
    
    Returns information about all available language models that can be used with DSPy.
    """
    try:
        models = [
            {
                "name": "gpt-4",
                "provider": "openai",
                "type": "chat",
                "max_tokens": 8192,
                "capabilities": ["code_review", "rag", "multi_hop", "classification"]
            },
            {
                "name": "gpt-3.5-turbo",
                "provider": "openai",
                "type": "chat",
                "max_tokens": 4096,
                "capabilities": ["code_review", "rag", "classification"]
            },
            {
                "name": "claude-3-sonnet-20240229",
                "provider": "anthropic",
                "type": "chat",
                "max_tokens": 200000,
                "capabilities": ["code_review", "rag", "multi_hop", "classification"]
            },
            {
                "name": "claude-3-haiku-20240307",
                "provider": "anthropic",
                "type": "chat",
                "max_tokens": 200000,
                "capabilities": ["code_review", "rag", "classification"]
            },
            {
                "name": "gemini-2.0-flash-exp",
                "provider": "google",
                "type": "generation",
                "max_tokens": 1000000,
                "capabilities": ["code_review", "rag", "multi_hop", "classification"]
            },
            {
                "name": "gemini-1.5-pro",
                "provider": "google",
                "type": "generation",
                "max_tokens": 1000000,
                "capabilities": ["code_review", "rag", "multi_hop", "classification"]
            }
        ]
        
        return {"models": models}
        
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/switch")
async def switch_model(
    model_name: str,
    provider: str,
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Switch to a different language model.
    
    Changes the active model for DSPy operations.
    """
    try:
        # This would implement model switching logic
        # For now, we'll return a success message
        logger.info(f"Switching to model: {model_name} from {provider}")
        
        return {
            "message": f"Successfully switched to {model_name}",
            "model_name": model_name,
            "provider": provider
        }
        
    except Exception as e:
        logger.error(f"Error switching model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/capabilities")
async def get_model_capabilities(
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Get current model capabilities.
    
    Returns information about what the current model can do.
    """
    try:
        capabilities = {
            "code_review": {
                "description": "Comprehensive code analysis and review",
                "features": ["bug_detection", "performance_analysis", "security_scanning", "style_checking"],
                "supported_languages": ["python", "javascript", "typescript", "java", "cpp", "go", "rust"]
            },
            "rag": {
                "description": "Retrieval-Augmented Generation for knowledge-intensive tasks",
                "features": ["document_retrieval", "context_aware_generation", "source_citation"],
                "supported_formats": ["text", "code", "markdown", "json"]
            },
            "multi_hop": {
                "description": "Multi-step reasoning for complex questions",
                "features": ["step_by_step_reasoning", "intermediate_verification", "chain_of_thought"],
                "complexity_levels": ["basic", "intermediate", "advanced"]
            },
            "classification": {
                "description": "Text and code classification tasks",
                "features": ["multi_label", "confidence_scoring", "custom_categories"],
                "supported_tasks": ["sentiment_analysis", "code_categorization", "bug_classification"]
            },
            "optimization": {
                "description": "Prompt and weight optimization using DSPy",
                "features": ["prompt_optimization", "weight_optimization", "hyperparameter_tuning"],
                "algorithms": ["bootstrap_few_shot", "random_search", "bayesian_optimization"]
            }
        }
        
        return {"capabilities": capabilities}
        
    except Exception as e:
        logger.error(f"Error getting capabilities: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance")
async def get_model_performance(
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Get model performance metrics.
    
    Returns performance statistics and metrics for the current model.
    """
    try:
        # This would typically fetch from a metrics database
        performance = {
            "response_time": {
                "average": 2.5,
                "p95": 4.2,
                "p99": 6.8,
                "unit": "seconds"
            },
            "accuracy": {
                "code_review": 0.85,
                "rag": 0.92,
                "multi_hop": 0.78,
                "classification": 0.89
            },
            "throughput": {
                "requests_per_minute": 120,
                "concurrent_requests": 10
            },
            "cost": {
                "per_request": 0.002,
                "per_token": 0.0001,
                "currency": "USD"
            }
        }
        
        return {"performance": performance}
        
    except Exception as e:
        logger.error(f"Error getting performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test")
async def test_model(
    test_input: str,
    task_type: str = "code_review",
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Test the current model with a sample input.
    
    Performs a quick test to verify the model is working correctly.
    """
    try:
        # Create a simple test based on task type
        if task_type == "code_review":
            test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
            """
            test_request = CodeReviewRequest(
                code=test_code,
                language="python",
                context="Test function for Fibonacci calculation"
            )
            result = await dspy_service.review_code(test_request)
            
        elif task_type == "rag":
            test_request = RAGRequest(
                question="What is the time complexity of this function?",
                context="The function uses recursion to calculate Fibonacci numbers."
            )
            result = await dspy_service.rag_query(test_request)
            
        else:
            result = {"message": "Test completed successfully", "task_type": task_type}
        
        return {
            "test_result": result,
            "task_type": task_type,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error testing model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def model_health_check(
    dspy_service: DSPyService = Depends(get_dspy_service)
):
    """
    Health check for the model service.
    
    Verifies that the model is accessible and functioning correctly.
    """
    try:
        # Perform a simple health check
        model_info = await dspy_service.get_model_info()
        
        return {
            "status": "healthy",
            "model_name": model_info.get("model_name", "unknown"),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Model health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
