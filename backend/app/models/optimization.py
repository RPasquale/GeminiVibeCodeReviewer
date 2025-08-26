"""
Pydantic models for optimization functionality.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class OptimizationStatus(str, Enum):
    """Optimization status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class OptimizationAlgorithm(str, Enum):
    """Optimization algorithm enumeration."""
    BOOTSTRAP_FEW_SHOT = "bootstrap_few_shot"
    RANDOM_SEARCH = "random_search"
    BAYESIAN_OPTIMIZATION = "bayesian_optimization"
    GENETIC_ALGORITHM = "genetic_algorithm"
    REINFORCEMENT_LEARNING = "reinforcement_learning"

class OptimizationRequest(BaseModel):
    """Request model for optimization."""
    target_module: str = Field(..., description="Module to optimize")
    optimization_algorithm: OptimizationAlgorithm = Field(..., description="Algorithm to use")
    training_data: List[Dict[str, Any]] = Field(..., description="Training data for optimization")
    validation_data: Optional[List[Dict[str, Any]]] = Field(default=None, description="Validation data")
    optimization_parameters: Dict[str, Any] = Field(default={}, description="Algorithm-specific parameters")
    max_iterations: int = Field(default=100, ge=1, le=1000, description="Maximum optimization iterations")
    evaluation_metric: str = Field(default="accuracy", description="Metric to optimize")
    constraints: Optional[Dict[str, Any]] = Field(default=None, description="Optimization constraints")
    early_stopping: bool = Field(default=True, description="Enable early stopping")
    save_intermediate_results: bool = Field(default=True, description="Save intermediate optimization results")

class OptimizationResponse(BaseModel):
    """Response model for optimization."""
    optimization_id: str = Field(..., description="Unique optimization ID")
    status: OptimizationStatus = Field(..., description="Current optimization status")
    target_module: str = Field(..., description="Module being optimized")
    algorithm: OptimizationAlgorithm = Field(..., description="Algorithm used")
    start_time: datetime = Field(..., description="Optimization start time")
    estimated_completion: Optional[datetime] = Field(default=None, description="Estimated completion time")
    current_iteration: Optional[int] = Field(default=None, description="Current iteration")
    total_iterations: int = Field(..., description="Total iterations")
    best_score: Optional[float] = Field(default=None, description="Best score achieved")
    optimization_history: List[Dict[str, Any]] = Field(default=[], description="Optimization history")
    optimized_module_path: Optional[str] = Field(default=None, description="Path to optimized module")

class OptimizationProgress(BaseModel):
    """Model for optimization progress updates."""
    optimization_id: str = Field(..., description="Optimization ID")
    status: OptimizationStatus = Field(..., description="Current status")
    iteration: int = Field(..., description="Current iteration")
    total_iterations: int = Field(..., description="Total iterations")
    current_score: float = Field(..., description="Current optimization score")
    best_score: float = Field(..., description="Best score so far")
    improvement: float = Field(..., description="Improvement from baseline")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class OptimizationResult(BaseModel):
    """Model for optimization results."""
    optimization_id: str = Field(..., description="Optimization ID")
    final_score: float = Field(..., description="Final optimization score")
    baseline_score: float = Field(..., description="Baseline score before optimization")
    improvement_percentage: float = Field(..., description="Percentage improvement")
    optimization_time: float = Field(..., description="Total optimization time")
    iterations_completed: int = Field(..., description="Number of iterations completed")
    best_parameters: Dict[str, Any] = Field(..., description="Best parameters found")
    optimization_history: List[Dict[str, Any]] = Field(..., description="Complete optimization history")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class HyperparameterTuning(BaseModel):
    """Model for hyperparameter tuning."""
    tuning_id: str = Field(..., description="Tuning ID")
    target_model: str = Field(..., description="Model to tune")
    hyperparameters: Dict[str, List[Any]] = Field(..., description="Hyperparameters to tune")
    tuning_method: str = Field(default="grid_search", description="Tuning method")
    cross_validation_folds: int = Field(default=5, description="Number of CV folds")
    evaluation_metric: str = Field(default="accuracy", description="Evaluation metric")
    max_trials: int = Field(default=100, description="Maximum trials")
    status: OptimizationStatus = Field(default=OptimizationStatus.PENDING)
    results: Optional[Dict[str, Any]] = Field(default=None, description="Tuning results")

class ModelComparison(BaseModel):
    """Model for comparing different models/optimizations."""
    comparison_id: str = Field(..., description="Comparison ID")
    models: List[str] = Field(..., description="Models to compare")
    evaluation_metrics: List[str] = Field(..., description="Metrics for comparison")
    test_data: List[Dict[str, Any]] = Field(..., description="Test data for evaluation")
    comparison_results: Dict[str, Dict[str, float]] = Field(..., description="Comparison results")
    winner: Optional[str] = Field(default=None, description="Best performing model")
    statistical_significance: Optional[Dict[str, float]] = Field(default=None, description="Statistical significance tests")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
