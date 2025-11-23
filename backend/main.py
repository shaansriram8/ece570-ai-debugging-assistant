"""FastAPI main application."""
import time
import logging
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings, get_active_models
from models import AnalyzeRequest, AnalyzeResponse, ModelMetadata, HealthResponse
from hf_client import call_multiple_models, build_analysis_prompt
from aggregator import process_model_outputs
from scorer import compute_heuristic_score
from cache import cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version
)

# CORS middleware (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    models = get_active_models()
    
    # Check if HF API is reachable (simple check)
    hf_reachable = bool(settings.hf_api_key)
    
    return HealthResponse(
        status="healthy",
        hf_api_reachable=hf_reachable,
        models_configured=models,
        backend_version=settings.api_version
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Main endpoint for code analysis.
    
    Takes code and error message, returns structured explanation and fix suggestion.
    """
    start_time = time.time()
    
    try:
        # Get active models based on request parameters
        if request.models:
            # User specified specific models
            models = request.models
        elif request.mode == "quick":
            # Quick mode: use only primary model
            models = [settings.primary_model] if settings.primary_model else []
        else:
            # Detailed mode (default): use both models
            models = get_active_models()
        
        if not models:
            raise HTTPException(
                status_code=500,
                detail="No models configured"
            )
        
        # Check cache
        cached_response = cache.get(request.code, request.error_message, models)
        if cached_response:
            logger.info("Returning cached response")
            # Reconstruct response model from cache
            return AnalyzeResponse(**cached_response)
        
        # Build prompt
        prompt = build_analysis_prompt(
            request.code,
            request.error_message,
            request.language
        )
        
        # Call models in parallel
        logger.info(f"Calling {len(models)} models in parallel")
        model_responses = await call_multiple_models(prompt, models)
        
        # Log model responses for debugging
        for model_name, (text, latency, error) in model_responses.items():
            if error:
                logger.warning(f"Model {model_name} returned error: {error}")
            elif text:
                logger.info(f"Model {model_name} returned response (length: {len(text) if text else 0})")
            else:
                logger.warning(f"Model {model_name} returned None (no error message)")
        
        # Parse and aggregate responses
        model_parsed, aggregated = process_model_outputs(model_responses)
        
        # Compute quality score (heuristic-based for live system)
        quality_score = compute_heuristic_score(aggregated)
        # Use model's own score if available, otherwise use heuristic
        final_score = aggregated.get("score", quality_score)
        
        # Build metadata
        total_latency_ms = (time.time() - start_time) * 1000
        per_model_latency = {
            model: latency
            for model, (_, latency, _) in model_responses.items()
        }
        
        # Check if any model used repair
        had_repair = any(had_repair for _, (_, had_repair) in model_parsed.items())
        
        meta = ModelMetadata(
            models_used=models,
            per_model_latency_ms=per_model_latency,
            total_latency_ms=total_latency_ms,
            had_repair=had_repair,
            from_cache=False,
            backend_version=settings.api_version
        )
        
        # Build response
        response = AnalyzeResponse(
            explanation=aggregated.get("explanation", ""),
            suggestion=aggregated.get("suggestion", ""),
            score=final_score,
            severity=aggregated.get("severity"),
            bug_type=aggregated.get("bug_type"),
            meta=meta
        )
        
        # Cache the response
        cache.set(
            request.code,
            request.error_message,
            models,
            response.model_dump()
        )
        
        logger.info(f"Analysis complete in {total_latency_ms:.2f}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error in analyze_code: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

