"""
Pydantic models for RAG (Retrieval-Augmented Generation) functionality.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class RAGRequest(BaseModel):
    """Request model for RAG queries."""
    question: str = Field(..., description="User question or query")
    context: Optional[str] = Field(default="", description="Additional context")
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum number of results to retrieve")
    search_type: str = Field(default="semantic", description="Search type: semantic, keyword, hybrid")
    include_sources: bool = Field(default=True, description="Whether to include source information")
    confidence_threshold: float = Field(default=0.7, ge=0, le=1, description="Minimum confidence threshold")

class RAGResponse(BaseModel):
    """Response model for RAG queries."""
    answer: str = Field(..., description="Generated answer based on retrieved context")
    sources: List[Dict[str, Any]] = Field(default=[], description="Source documents used")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score for the answer")
    retrieved_documents: List[Dict[str, Any]] = Field(default=[], description="Retrieved documents")
    processing_time: float = Field(..., description="Time taken to process the query")
    model_used: str = Field(..., description="Model used for generation")

class DocumentChunk(BaseModel):
    """Model for document chunks in vector database."""
    id: str = Field(..., description="Unique identifier for the chunk")
    content: str = Field(..., description="Text content of the chunk")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")
    embedding: Optional[List[float]] = Field(default=None, description="Vector embedding")
    source: str = Field(..., description="Source document")
    chunk_index: int = Field(..., description="Index of this chunk in the source")

class VectorSearchRequest(BaseModel):
    """Request model for vector search."""
    query: str = Field(..., description="Search query")
    collection_name: str = Field(..., description="Name of the vector collection")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of top results")
    similarity_threshold: float = Field(default=0.7, ge=0, le=1, description="Minimum similarity score")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filters")

class VectorSearchResponse(BaseModel):
    """Response model for vector search."""
    results: List[DocumentChunk] = Field(..., description="Search results")
    query_embedding: Optional[List[float]] = Field(default=None, description="Query embedding")
    total_results: int = Field(..., description="Total number of results found")
    search_time: float = Field(..., description="Time taken for search")

class DocumentIngestionRequest(BaseModel):
    """Request model for document ingestion."""
    documents: List[Dict[str, Any]] = Field(..., description="Documents to ingest")
    collection_name: str = Field(..., description="Target collection name")
    chunk_size: int = Field(default=1000, description="Size of text chunks")
    chunk_overlap: int = Field(default=200, description="Overlap between chunks")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")

class DocumentIngestionResponse(BaseModel):
    """Response model for document ingestion."""
    ingested_count: int = Field(..., description="Number of documents ingested")
    chunks_created: int = Field(..., description="Number of chunks created")
    collection_name: str = Field(..., description="Name of the collection")
    processing_time: float = Field(..., description="Time taken for ingestion")
