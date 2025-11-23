"""Pydantic models for request/response schemas."""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """Request model for the /analyze endpoint."""
    code: str = Field(..., description="Source code with the bug")
    error_message: str = Field(..., description="Error message or stack trace")
    language: Optional[str] = Field(None, description="Programming language (optional)")
    mode: Optional[str] = Field("detailed", description="Analysis mode: 'quick' (single model) or 'detailed' (both models)")
    models: Optional[List[str]] = Field(None, description="Optional: Specific models to use (overrides mode if provided)")


class ModelMetadata(BaseModel):
    """Metadata about model responses."""
    models_used: List[str] = Field(default_factory=list)
    per_model_latency_ms: Dict[str, float] = Field(default_factory=dict)
    total_latency_ms: float = 0.0
    had_repair: bool = False
    from_cache: bool = False
    backend_version: Optional[str] = None


class AnalyzeResponse(BaseModel):
    """Response model for the /analyze endpoint."""
    explanation: str = Field(..., description="Root-cause explanation of the bug")
    suggestion: str = Field(..., description="Concrete suggested fix or next debugging steps")
    score: int = Field(..., ge=0, le=100, description="Quality/confidence score (0-100)")
    severity: Optional[str] = Field(None, description="Bug severity level")
    bug_type: Optional[str] = Field(None, description="Type of bug")
    meta: ModelMetadata = Field(default_factory=ModelMetadata)


class HealthResponse(BaseModel):
    """Response model for the /health endpoint."""
    status: str
    hf_api_reachable: bool
    models_configured: List[str]
    backend_version: str


class EvaluationExample(BaseModel):
    """Single example in the evaluation dataset."""
    code: str
    error_message: str
    gold_explanation: str
    gold_suggestion: str
    language: Optional[str] = None


class EvaluationResult(BaseModel):
    """Result of evaluating a single example."""
    example_id: int
    valid_json: bool
    explanation_score: float
    suggestion_score: float
    overall_score: float
    latency_ms: float
    models_used: List[str]
    had_repair: bool


class EvaluationSummary(BaseModel):
    """Summary statistics from evaluation run."""
    total_examples: int
    valid_json_count: int
    valid_json_rate: float
    mean_explanation_score: float
    mean_suggestion_score: float
    mean_overall_score: float
    mean_latency_ms: float
    per_model_stats: Dict[str, Dict[str, Any]]

