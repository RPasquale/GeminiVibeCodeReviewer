"""
Pydantic models for training and fine-tuning functionality.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class TrainingStatus(str, Enum):
    """Training status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ModelType(str, Enum):
    """Model type enumeration."""
    CODE_REVIEW = "code_review"
    RAG = "rag"
    MULTI_HOP = "multi_hop"
    CLASSIFICATION = "classification"
    GENERATION = "generation"

class OptimizationType(str, Enum):
    """Optimization type enumeration."""
    PROMPT_OPTIMIZATION = "prompt_optimization"
    WEIGHT_OPTIMIZATION = "weight_optimization"
    HYBRID_OPTIMIZATION = "hybrid_optimization"

class TrainingRequest(BaseModel):
    """Request model for training/fine-tuning."""
    model_type: ModelType = Field(..., description="Type of model to train")
    training_data: List[Dict[str, Any]] = Field(..., description="Training data")
    validation_data: Optional[List[Dict[str, Any]]] = Field(default=None, description="Validation data")
    hyperparameters: Dict[str, Any] = Field(default={}, description="Training hyperparameters")
    optimization_type: OptimizationType = Field(default=OptimizationType.PROMPT_OPTIMIZATION)
    epochs: int = Field(default=10, ge=1, le=100, description="Number of training epochs")
    batch_size: int = Field(default=32, ge=1, le=128, description="Training batch size")
    learning_rate: float = Field(default=1e-5, ge=1e-7, le=1e-2, description="Learning rate")
    evaluation_metrics: List[str] = Field(default=["accuracy"], description="Metrics to evaluate")
    save_checkpoints: bool = Field(default=True, description="Whether to save checkpoints")
    early_stopping: bool = Field(default=True, description="Enable early stopping")

class TrainingResponse(BaseModel):
    """Response model for training/fine-tuning."""
    training_id: str = Field(..., description="Unique training ID")
    status: TrainingStatus = Field(..., description="Current training status")
    model_type: ModelType = Field(..., description="Type of model being trained")
    start_time: datetime = Field(..., description="Training start time")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion time")
    current_epoch: Optional[int] = Field(default=None, description="Current training epoch")
    total_epochs: int = Field(..., description="Total number of epochs")
    metrics: Dict[str, float] = Field(default={}, description="Current training metrics")
    model_path: Optional[str] = Field(default=None, description="Path to saved model")

class TrainingProgress(BaseModel):
    """Model for training progress updates."""
    training_id: str = Field(..., description="Training ID")
    status: TrainingStatus = Field(..., description="Current status")
    epoch: int = Field(..., description="Current epoch")
    total_epochs: int = Field(..., description="Total epochs")
    loss: float = Field(..., description="Current loss")
    accuracy: Optional[float] = Field(default=None, description="Current accuracy")
    validation_loss: Optional[float] = Field(default=None, description="Validation loss")
    validation_accuracy: Optional[float] = Field(default=None, description="Validation accuracy")
    learning_rate: float = Field(..., description="Current learning rate")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ModelEvaluation(BaseModel):
    """Model for model evaluation results."""
    model_id: str = Field(..., description="Model identifier")
    evaluation_metrics: Dict[str, float] = Field(..., description="Evaluation metrics")
    test_data_size: int = Field(..., description="Size of test dataset")
    evaluation_time: float = Field(..., description="Time taken for evaluation")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    detailed_results: Optional[Dict[str, Any]] = Field(default=None, description="Detailed evaluation results")

class ModelDeployment(BaseModel):
    """Model for model deployment."""
    model_id: str = Field(..., description="Model identifier")
    deployment_name: str = Field(..., description="Name for the deployment")
    environment: str = Field(default="production", description="Deployment environment")
    version: str = Field(..., description="Model version")
    endpoint_url: Optional[str] = Field(default=None, description="Deployment endpoint URL")
    status: str = Field(default="pending", description="Deployment status")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TrainingDataset(BaseModel):
    """Model for training dataset."""
    dataset_id: str = Field(..., description="Dataset identifier")
    name: str = Field(..., description="Dataset name")
    description: str = Field(..., description="Dataset description")
    size: int = Field(..., description="Number of samples")
    model_type: ModelType = Field(..., description="Target model type")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
