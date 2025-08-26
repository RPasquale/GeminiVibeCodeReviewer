"""
Training and fine-tuning API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
import uuid
from datetime import datetime
from loguru import logger

from app.models.training import (
    TrainingRequest, 
    TrainingResponse, 
    TrainingProgress,
    ModelEvaluation,
    ModelDeployment,
    TrainingDataset
)
from app.services.training_service import TrainingService

router = APIRouter()

async def get_training_service() -> TrainingService:
    """Dependency to get training service."""
    return TrainingService()

@router.post("/start", response_model=TrainingResponse)
async def start_training(
    request: TrainingRequest,
    background_tasks: BackgroundTasks,
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Start a new training job using DSPy.
    
    This endpoint initiates model training/fine-tuning with DSPy's optimization capabilities.
    """
    try:
        # Generate training ID
        training_id = str(uuid.uuid4())
        
        # Create training response
        response = TrainingResponse(
            training_id=training_id,
            status="pending",
            model_type=request.model_type,
            start_time=datetime.utcnow(),
            total_epochs=request.epochs
        )
        
        # Start training in background
        background_tasks.add_task(
            training_service.train_model,
            training_id,
            request
        )
        
        logger.info(f"Started training job: {training_id}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error starting training: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{training_id}", response_model=TrainingProgress)
async def get_training_status(
    training_id: str,
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Get the status of a training job.
    
    Returns current progress and metrics for the specified training job.
    """
    try:
        progress = await training_service.get_training_progress(training_id)
        
        if not progress:
            raise HTTPException(status_code=404, detail="Training job not found")
        
        return progress
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting training status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs")
async def list_training_jobs(
    training_service: TrainingService = Depends(get_training_service)
):
    """
    List all training jobs.
    
    Returns a list of all training jobs with their status and basic information.
    """
    try:
        jobs = await training_service.list_training_jobs()
        return {"jobs": jobs}
        
    except Exception as e:
        logger.error(f"Error listing training jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cancel/{training_id}")
async def cancel_training(
    training_id: str,
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Cancel a running training job.
    
    Stops the specified training job if it's currently running.
    """
    try:
        success = await training_service.cancel_training(training_id)
        
        if success:
            return {"message": f"Training job {training_id} cancelled successfully"}
        else:
            raise HTTPException(status_code=404, detail="Training job not found or already completed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling training: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evaluate/{model_id}", response_model=ModelEvaluation)
async def evaluate_model(
    model_id: str,
    test_data: List[dict],
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Evaluate a trained model.
    
    Performs evaluation on the specified model using the provided test data.
    """
    try:
        evaluation = await training_service.evaluate_model(model_id, test_data)
        
        if not evaluation:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return evaluation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error evaluating model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/deploy/{model_id}", response_model=ModelDeployment)
async def deploy_model(
    model_id: str,
    deployment_name: str,
    environment: str = "production",
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Deploy a trained model.
    
    Deploys the specified model to the specified environment.
    """
    try:
        deployment = await training_service.deploy_model(
            model_id, 
            deployment_name, 
            environment
        )
        
        if not deployment:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return deployment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deploying model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/datasets")
async def list_datasets(
    training_service: TrainingService = Depends(get_training_service)
):
    """
    List available training datasets.
    
    Returns information about available datasets for training.
    """
    try:
        datasets = await training_service.list_datasets()
        return {"datasets": datasets}
        
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/datasets", response_model=TrainingDataset)
async def create_dataset(
    name: str,
    description: str,
    model_type: str,
    data: List[dict],
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Create a new training dataset.
    
    Creates and stores a new dataset for training purposes.
    """
    try:
        dataset = TrainingDataset(
            dataset_id=str(uuid.uuid4()),
            name=name,
            description=description,
            size=len(data),
            model_type=model_type,
            metadata={"data_preview": data[:5]}  # Store first 5 items as preview
        )
        
        # Store dataset (this would typically save to database)
        await training_service.save_dataset(dataset, data)
        
        return dataset
        
    except Exception as e:
        logger.error(f"Error creating dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/datasets/{dataset_id}")
async def delete_dataset(
    dataset_id: str,
    training_service: TrainingService = Depends(get_training_service)
):
    """
    Delete a training dataset.
    
    Removes the specified dataset and all associated data.
    """
    try:
        success = await training_service.delete_dataset(dataset_id)
        
        if success:
            return {"message": f"Dataset {dataset_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Dataset not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))
