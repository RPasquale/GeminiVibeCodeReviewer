"""
Pydantic models for code review functionality.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class FeedbackItem(BaseModel):
    """Individual feedback item."""
    category: str = Field(..., description="Category of feedback (e.g., 'Bugs', 'Performance', 'Security')")
    details: str = Field(..., description="Detailed feedback description")
    severity: str = Field(default="medium", description="Severity level: low, medium, high, critical")
    line_numbers: Optional[List[int]] = Field(default=None, description="Relevant line numbers")
    suggestions: Optional[List[str]] = Field(default=None, description="Specific suggestions for improvement")

class CodeReviewRequest(BaseModel):
    """Request model for code review."""
    code: str = Field(..., description="The code to review")
    language: str = Field(..., description="Programming language")
    context: Optional[str] = Field(default="", description="Additional context about the codebase")
    review_type: str = Field(default="comprehensive", description="Type of review: comprehensive, security, performance, style")
    include_suggestions: bool = Field(default=True, description="Whether to include improvement suggestions")
    roast_mode: bool = Field(default=False, description="Enable humorous/roast mode for feedback")

class CodeReviewResponse(BaseModel):
    """Response model for code review."""
    summary: str = Field(..., description="Brief summary of the code quality")
    feedback: List[FeedbackItem] = Field(..., description="Detailed feedback items")
    score: float = Field(..., ge=1, le=10, description="Overall quality score from 1-10")
    suggestions: List[str] = Field(default=[], description="General improvement suggestions")
    model_used: str = Field(..., description="Name of the model used for review")
    review_timestamp: datetime = Field(default_factory=datetime.utcnow)
    processing_time: Optional[float] = Field(default=None, description="Time taken to process the review")
    confidence: float = Field(default=0.8, ge=0, le=1, description="Confidence in the review")

class BatchCodeReviewRequest(BaseModel):
    """Request model for batch code review."""
    files: List[Dict[str, str]] = Field(..., description="List of files with name and content")
    language: str = Field(..., description="Programming language for all files")
    context: Optional[str] = Field(default="", description="Additional context about the codebase")
    review_type: str = Field(default="comprehensive", description="Type of review")
    include_cross_file_analysis: bool = Field(default=True, description="Analyze relationships between files")

class BatchCodeReviewResponse(BaseModel):
    """Response model for batch code review."""
    file_reviews: List[CodeReviewResponse] = Field(..., description="Individual file reviews")
    overall_summary: str = Field(..., description="Overall summary across all files")
    cross_file_issues: List[Dict[str, Any]] = Field(default=[], description="Issues spanning multiple files")
    total_score: float = Field(..., description="Average score across all files")
    processing_time: float = Field(..., description="Total processing time")
