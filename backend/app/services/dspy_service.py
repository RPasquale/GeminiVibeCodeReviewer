"""
Core DSPy service for advanced LLM functionality including RAG, fine-tuning, and optimization.
"""

import dspy
from dspy import Predict, ChainOfThought, ReAct, MultiChainComparison
from dspy.teleprompt import BootstrapFewShot, BootstrapFewShotWithRandomSearch
from dspy.evaluate import Evaluate
from dspy.optimize import BootstrapFewShotWithRandomSearch
from typing import List, Dict, Any, Optional
import json
import asyncio
from loguru import logger

from app.core.config import settings
from app.models.code_review import CodeReviewRequest, CodeReviewResponse
from app.models.rag import RAGRequest, RAGResponse
from app.models.training import TrainingRequest, TrainingResponse
from app.models.optimization import OptimizationRequest, OptimizationResponse

class CodeReviewSignature(dspy.Signature):
    """Signature for code review task."""
    code = dspy.InputField(desc="The code to review")
    language = dspy.InputField(desc="Programming language of the code")
    context = dspy.InputField(desc="Additional context about the codebase", default="")
    
    summary = dspy.OutputField(desc="Brief summary of the code quality")
    feedback = dspy.OutputField(desc="Detailed feedback with categories")
    score = dspy.OutputField(desc="Overall quality score from 1-10")
    suggestions = dspy.OutputField(desc="Specific improvement suggestions")

class RAGSignature(dspy.Signature):
    """Signature for RAG (Retrieval-Augmented Generation) task."""
    question = dspy.InputField(desc="User question or query")
    context = dspy.InputField(desc="Retrieved relevant context")
    
    answer = dspy.OutputField(desc="Comprehensive answer based on context")
    sources = dspy.OutputField(desc="Sources used for the answer")
    confidence = dspy.OutputField(desc="Confidence score from 0-1")

class MultiHopSignature(dspy.Signature):
    """Signature for multi-hop reasoning tasks."""
    question = dspy.InputField(desc="Complex question requiring multi-step reasoning")
    intermediate_steps = dspy.InputField(desc="Intermediate reasoning steps")
    
    final_answer = dspy.OutputField(desc="Final answer after multi-step reasoning")
    reasoning_chain = dspy.OutputField(desc="Complete reasoning chain")

class DSPyService:
    """Main DSPy service for handling all LLM operations."""
    
    def __init__(self):
        """Initialize DSPy service with models and optimizers."""
        self.setup_models()
        self.setup_modules()
        self.setup_optimizers()
        logger.info(f"DSPy service initialized with {settings.llm_provider} provider")
    
    def setup_models(self):
        """Setup different language models for various tasks."""
        try:
            if settings.llm_provider == "ollama":
                # Configure DSPy with Ollama for local development
                dspy.configure(lm=dspy.Ollama(
                    model=settings.ollama_model,
                    base_url=settings.ollama_base_url,
                    max_tokens=settings.dspy_max_tokens,
                    temperature=settings.dspy_temperature
                ))
                logger.info(f"Configured DSPy with Ollama model: {settings.ollama_model}")
                
            elif settings.llm_provider == "openai" and settings.openai_api_key:
                dspy.configure(lm=dspy.OpenAI(
                    model=settings.llm_model,
                    api_key=settings.openai_api_key,
                    max_tokens=settings.dspy_max_tokens,
                    temperature=settings.dspy_temperature
                ))
                logger.info(f"Configured DSPy with OpenAI model: {settings.llm_model}")
                
            elif settings.llm_provider == "anthropic" and settings.anthropic_api_key:
                dspy.configure(lm=dspy.Anthropic(
                    model=settings.llm_model,
                    api_key=settings.anthropic_api_key,
                    max_tokens=settings.dspy_max_tokens
                ))
                logger.info(f"Configured DSPy with Anthropic model: {settings.llm_model}")
                
            elif settings.llm_provider == "google" and settings.google_api_key:
                dspy.configure(lm=dspy.GoogleGenerativeAI(
                    model=settings.llm_model,
                    api_key=settings.google_api_key
                ))
                logger.info(f"Configured DSPy with Google model: {settings.llm_model}")
                
            else:
                logger.warning(f"No valid configuration for {settings.llm_provider}, falling back to Ollama")
                # Fallback to Ollama
                dspy.configure(lm=dspy.Ollama(
                    model="deepseek-coder:1.3b",
                    base_url="http://localhost:11434",
                    max_tokens=settings.dspy_max_tokens,
                    temperature=settings.dspy_temperature
                ))
                
        except Exception as e:
            logger.error(f"Error setting up models: {e}")
            raise
    
    def setup_modules(self):
        """Setup DSPy modules for different tasks."""
        # Code review module
        self.code_reviewer = Predict(CodeReviewSignature)
        
        # RAG module
        self.rag_module = ChainOfThought(RAGSignature)
        
        # Multi-hop reasoning module
        self.multi_hop = ReAct(MultiHopSignature)
        
        # Multi-chain comparison for complex tasks
        self.multi_chain = MultiChainComparison(
            signature=CodeReviewSignature,
            M=3  # Number of chains to compare
        )
        
        logger.info("DSPy modules setup complete")
    
    def setup_optimizers(self):
        """Setup DSPy optimizers for prompt and weight optimization."""
        # Bootstrap few-shot optimizer
        self.bootstrap_optimizer = BootstrapFewShot(
            metric=self.evaluate_code_review,
            max_bootstrapped_demos=8,
            max_labeled_demos=4
        )
        
        # Random search optimizer
        self.random_search_optimizer = BootstrapFewShotWithRandomSearch(
            metric=self.evaluate_code_review,
            max_bootstrapped_demos=8,
            max_labeled_demos=4,
            num_candidate_programs=10,
            num_threads=4
        )
        
        logger.info("DSPy optimizers setup complete")
    
    async def review_code(self, request: CodeReviewRequest) -> CodeReviewResponse:
        """Perform code review using DSPy."""
        try:
            # Prepare input
            input_data = {
                "code": request.code,
                "language": request.language,
                "context": request.context or ""
            }
            
            # Use optimized code reviewer if available
            if hasattr(self, 'optimized_reviewer'):
                result = self.optimized_reviewer(**input_data)
            else:
                result = self.code_reviewer(**input_data)
            
            # Parse and format response
            feedback_items = []
            if hasattr(result, 'feedback') and result.feedback:
                if isinstance(result.feedback, str):
                    # Parse JSON if it's a string
                    try:
                        feedback_data = json.loads(result.feedback)
                        feedback_items = feedback_data
                    except:
                        feedback_items = [{"category": "General", "details": result.feedback}]
                else:
                    feedback_items = result.feedback
            
            return CodeReviewResponse(
                summary=result.summary,
                feedback=feedback_items,
                score=getattr(result, 'score', 7),
                suggestions=getattr(result, 'suggestions', []),
                model_used=f"{settings.llm_provider}:{settings.llm_model}"
            )
            
        except Exception as e:
            logger.error(f"Error in code review: {e}")
            raise
    
    async def rag_query(self, request: RAGRequest) -> RAGResponse:
        """Perform RAG (Retrieval-Augmented Generation) query."""
        try:
            # This would integrate with a vector database for retrieval
            # For now, we'll use the provided context
            result = self.rag_module(
                question=request.question,
                context=request.context or "No additional context provided."
            )
            
            return RAGResponse(
                answer=result.answer,
                sources=result.sources or [],
                confidence=getattr(result, 'confidence', 0.8),
                model_used=f"{settings.llm_provider}:{settings.llm_model}"
            )
            
        except Exception as e:
            logger.error(f"Error in RAG query: {e}")
            raise
    
    async def multi_hop_reasoning(self, question: str) -> Dict[str, Any]:
        """Perform multi-hop reasoning for complex questions."""
        try:
            result = self.multi_hop(question=question)
            
            return {
                "answer": result.final_answer,
                "reasoning_chain": result.reasoning_chain,
                "intermediate_steps": getattr(result, 'intermediate_steps', []),
                "model_used": f"{settings.llm_provider}:{settings.llm_model}"
            }
            
        except Exception as e:
            logger.error(f"Error in multi-hop reasoning: {e}")
            raise
    
    async def optimize_code_reviewer(self, training_data: List[Dict[str, Any]]) -> bool:
        """Optimize the code reviewer using DSPy optimizers."""
        try:
            # Convert training data to DSPy format
            trainset = []
            for item in training_data:
                trainset.append(dspy.Example(
                    code=item['code'],
                    language=item['language'],
                    context=item.get('context', ''),
                    summary=item['expected_summary'],
                    feedback=item['expected_feedback'],
                    score=item['expected_score'],
                    suggestions=item.get('expected_suggestions', [])
                ).with_inputs('code', 'language', 'context'))
            
            # Optimize using bootstrap few-shot
            self.optimized_reviewer = self.bootstrap_optimizer.compile(
                self.code_reviewer,
                trainset=trainset
            )
            
            logger.info("Code reviewer optimization complete")
            return True
            
        except Exception as e:
            logger.error(f"Error optimizing code reviewer: {e}")
            return False
    
    def evaluate_code_review(self, example, pred, trace=None):
        """Evaluation metric for code review quality."""
        # Simple evaluation based on output completeness
        score = 0.0
        
        if hasattr(pred, 'summary') and pred.summary:
            score += 0.3
        
        if hasattr(pred, 'feedback') and pred.feedback:
            score += 0.4
        
        if hasattr(pred, 'score') and pred.score:
            score += 0.2
        
        if hasattr(pred, 'suggestions') and pred.suggestions:
            score += 0.1
        
        return score
    
    async def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model configuration."""
        return {
            "provider": settings.llm_provider,
            "model_name": settings.llm_model,
            "max_tokens": settings.dspy_max_tokens,
            "temperature": settings.dspy_temperature,
            "has_optimized_reviewer": hasattr(self, 'optimized_reviewer'),
            "available_modules": [
                "code_reviewer",
                "rag_module", 
                "multi_hop",
                "multi_chain"
            ]
        }
