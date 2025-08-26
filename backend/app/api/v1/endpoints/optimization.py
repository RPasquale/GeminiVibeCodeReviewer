"""
Optimization API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
import uuid
from datetime import datetime
from loguru import logger

from app.models.optimization import (
    OptimizationRequest, 
    OptimizationResponse, 
    OptimizationProgress,
    OptimizationResult,
    HyperparameterTuning,
    ModelComparison
)
from app.services.optimization_service import OptimizationService

router = APIRouter()

async def get_optimization_service() -> OptimizationService:
    """Dependency to get optimization service."""
    return OptimizationService()

@router.post("/start", response_model=OptimizationResponse)
async def start_optimization(
    request: OptimizationRequest,
    background_tasks: BackgroundTasks,
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    Start a new optimization job using DSPy.
    
    This endpoint initiates prompt or weight optimization using DSPy's optimization algorithms.
    """
    try:
        # Generate optimization ID
        optimization_id = str(uuid.uuid4())
        
        # Create optimization response
        response = OptimizationResponse(
            optimization_id=optimization_id,
            status="pending",
            target_module=request.target_module,
            algorithm=request.optimization_algorithm,
            start_time=datetime.utcnow(),
            total_iterations=request.max_iterations
        )
        
        # Start optimization in background
        background_tasks.add_task(
            optimization_service.optimize_module,
            optimization_id,
            request
        )
        
        logger.info(f"Started optimization job: {optimization_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error starting optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{optimization_id}", response_model=OptimizationProgress)
async def get_optimization_status(
    optimization_id: str,
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    Get the status of an optimization job.
    
    Returns current progress and metrics for the specified optimization job.
    """
    try:
        progress = await optimization_service.get_optimization_progress(optimization_id)
        
        if not progress:
            raise HTTPException(status_code=404, detail="Optimization job not found")
        
        return progress
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting optimization status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs")
async def list_optimization_jobs(
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    List all optimization jobs.
    
    Returns a list of all optimization jobs with their status and basic information.
    """
    try:
        jobs = await optimization_service.list_optimization_jobs()
        return {"jobs": jobs}
        
    except Exception as e:
        logger.error(f"Error listing optimization jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cancel/{optimization_id}")
async def cancel_optimization(
    optimization_id: str,
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    Cancel a running optimization job.
    
    Stops the specified optimization job if it's currently running.
    """
    try:
        success = await optimization_service.cancel_optimization(optimization_id)
        
        if success:
            return {"message": f"Optimization job {optimization_id} cancelled successfully"}
        else:
            raise HTTPException(status_code=404, detail="Optimization job not found or already completed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{optimization_id}", response_model=OptimizationResult)
async def get_optimization_results(
    optimization_id: str,
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    Get the results of a completed optimization job.
    
    Returns detailed results and metrics for the specified optimization job.
    """
    try:
        results = await optimization_service.get_optimization_results(optimization_id)
        
        if not results:
            raise HTTPException(status_code=404, detail="Optimization job not found or not completed")
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting optimization results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hyperparameter-tuning", response_model=HyperparameterTuning)
async def start_hyperparameter_tuning(
    target_model: str,
    hyperparameters: dict,
    tuning_method: str = "grid_search",
    max_trials: int = 100,
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    Start hyperparameter tuning.
    
    Initiates hyperparameter optimization for the specified model.
    """
    try:
        tuning_id = str(uuid.uuid4())
        
        tuning = HyperparameterTuning(
            tuning_id=tuning_id,
            target_model=target_model,
            hyperparameters=hyperparameters,
            tuning_method=tuning_method,
            max_trials=max_trials
        )
        
        # Start tuning in background
        background_tasks.add_task(
            optimization_service.tune_hyperparameters,
            tuning_id,
            tuning
        )
        
        logger.info(f"Started hyperparameter tuning: {tuning_id}")
        
        return tuning
        
    except Exception as e:
        logger.error(f"Error starting hyperparameter tuning: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare-models", response_model=ModelComparison)
async def compare_models(
    models: List[str],
    evaluation_metrics: List[str],
    test_data: List[dict],
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    Compare multiple models.
    
    Performs comprehensive comparison of multiple models using specified metrics.
    """
    try:
        comparison_id = str(uuid.uuid4())
        
        comparison = ModelComparison(
            comparison_id=comparison_id,
            models=models,
            evaluation_metrics=evaluation_metrics,
            test_data=test_data,
            comparison_results={}
        )
        
        # Perform comparison
        results = await optimization_service.compare_models(
            models, 
            evaluation_metrics, 
            test_data
        )
        
        comparison.comparison_results = results
        comparison.winner = max(results.keys(), key=lambda k: results[k].get('accuracy', 0))
        
        return comparison
        
    except Exception as e:
        logger.error(f"Error comparing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/algorithms")
async def list_optimization_algorithms():
    """
    List available optimization algorithms.
    
    Returns information about available DSPy optimization algorithms.
    """
    try:
        algorithms = [
            {
                "name": "bootstrap_few_shot",
                "description": "Bootstrap few-shot optimization for prompt improvement",
                "type": "prompt_optimization",
                "parameters": ["max_bootstrapped_demos", "max_labeled_demos"]
            },
            {
                "name": "random_search",
                "description": "Random search optimization with few-shot learning",
                "type": "prompt_optimization",
                "parameters": ["num_candidate_programs", "num_threads"]
            },
            {
                "name": "bayesian_optimization",
                "description": "Bayesian optimization for hyperparameter tuning",
                "type": "weight_optimization",
                "parameters": ["n_trials", "timeout"]
            },
            {
                "name": "genetic_algorithm",
                "description": "Genetic algorithm for prompt evolution",
                "type": "prompt_optimization",
                "parameters": ["population_size", "generations"]
            },
            {
                "name": "reinforcement_learning",
                "description": "Reinforcement learning for policy optimization",
                "type": "hybrid_optimization",
                "parameters": ["learning_rate", "episodes"]
            }
        ]
        
        return {"algorithms": algorithms}
        
    except Exception as e:
        logger.error(f"Error listing algorithms: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-performance")
async def analyze_performance(
    module_name: str,
    test_data: List[dict],
    optimization_service: OptimizationService = Depends(get_optimization_service)
):
    """
    Analyze module performance.
    
    Performs detailed performance analysis of a module to identify optimization opportunities.
    """
    try:
        analysis = await optimization_service.analyze_performance(module_name, test_data)
        
        return {
            "module_name": module_name,
            "analysis": analysis,
            "recommendations": analysis.get("recommendations", []),
            "optimization_potential": analysis.get("optimization_potential", 0.0)
        }
        
    except Exception as e:
        logger.error(f"Error analyzing performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))
