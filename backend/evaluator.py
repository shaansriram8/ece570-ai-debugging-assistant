"""Evaluation pipeline for offline evaluation."""
import asyncio
import json
import logging
import time
from typing import List, Dict, Any, Tuple
from pathlib import Path

from config import settings, get_active_models
from models import EvaluationExample, EvaluationResult, EvaluationSummary
from hf_client import call_multiple_models, build_analysis_prompt
from aggregator import process_model_outputs
from scorer import score_explanation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def evaluate_single_example(
    example: EvaluationExample,
    example_id: int
) -> EvaluationResult:
    """
    Evaluate a single example from the evaluation dataset.
    
    Returns:
        EvaluationResult with scores and metadata
    """
    start_time = time.time()
    
    # Get active models
    models = get_active_models()
    
    # Build prompt
    prompt = build_analysis_prompt(
        example.code,
        example.error_message,
        example.language
    )
    
    # Call models
    model_responses = await call_multiple_models(prompt, models)
    
    # Parse and aggregate
    model_parsed, aggregated = process_model_outputs(model_responses)
    
    # Check if we got valid JSON
    valid_json = aggregated.get("explanation") != "" and aggregated.get("suggestion") != ""
    
    # Score against gold standard
    gold = {
        "explanation": example.gold_explanation,
        "suggestion": example.gold_suggestion
    }
    
    scores = score_explanation(aggregated, gold)
    
    latency_ms = (time.time() - start_time) * 1000
    
    # Check if any model used repair
    had_repair = any(had_repair for _, (_, had_repair) in model_parsed.items())
    
    return EvaluationResult(
        example_id=example_id,
        valid_json=valid_json,
        explanation_score=scores["explanation_score"],
        suggestion_score=scores["suggestion_score"],
        overall_score=scores["overall_score"],
        latency_ms=latency_ms,
        models_used=models,
        had_repair=had_repair
    )


async def run_evaluation(dataset_path: str = None) -> Tuple[EvaluationSummary, List[EvaluationResult]]:
    """
    Run evaluation on the full dataset.
    
    Args:
        dataset_path: Path to evaluation dataset JSON file
    
    Returns:
        Tuple of (EvaluationSummary with aggregate statistics, List[EvaluationResult] with per-example results)
    """
    dataset_path = dataset_path or settings.evaluation_dataset_path
    
    # Load dataset
    with open(dataset_path, 'r') as f:
        data = json.load(f)
    
    examples = [EvaluationExample(**item) for item in data]
    
    logger.info(f"Evaluating {len(examples)} examples...")
    
    # Evaluate all examples
    tasks = [
        evaluate_single_example(example, i)
        for i, example in enumerate(examples)
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Compute statistics
    valid_json_count = sum(1 for r in results if r.valid_json)
    valid_json_rate = (valid_json_count / len(results)) * 100 if results else 0
    
    explanation_scores = [r.explanation_score for r in results]
    suggestion_scores = [r.suggestion_score for r in results]
    overall_scores = [r.overall_score for r in results]
    latencies = [r.latency_ms for r in results]
    
    mean_explanation_score = sum(explanation_scores) / len(explanation_scores) if explanation_scores else 0
    mean_suggestion_score = sum(suggestion_scores) / len(suggestion_scores) if suggestion_scores else 0
    mean_overall_score = sum(overall_scores) / len(overall_scores) if overall_scores else 0
    mean_latency_ms = sum(latencies) / len(latencies) if latencies else 0
    
    # Per-model statistics (simplified - would need more detailed tracking)
    per_model_stats = {}
    for model in get_active_models():
        per_model_stats[model] = {
            "used_count": len([r for r in results if model in r.models_used]),
            "mean_latency_ms": mean_latency_ms  # Simplified
        }
    
    summary = EvaluationSummary(
        total_examples=len(examples),
        valid_json_count=valid_json_count,
        valid_json_rate=valid_json_rate,
        mean_explanation_score=mean_explanation_score,
        mean_suggestion_score=mean_suggestion_score,
        mean_overall_score=mean_overall_score,
        mean_latency_ms=mean_latency_ms,
        per_model_stats=per_model_stats
    )
    
    return summary, results


def save_evaluation_results(
    summary: EvaluationSummary,
    results: List[EvaluationResult],
    output_path: str = "evaluation_results.json"
):
    """Save evaluation results to JSON file."""
    output = {
        "summary": summary.model_dump(),
        "results": [r.model_dump() for r in results]
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Evaluation results saved to {output_path}")


async def main():
    """CLI entry point for evaluation."""
    print("Starting evaluation...")
    summary, results = await run_evaluation()
    
    print("\n=== Evaluation Summary ===")
    print(f"Total examples: {summary.total_examples}")
    print(f"Valid JSON rate: {summary.valid_json_rate:.2f}%")
    print(f"Mean explanation score: {summary.mean_explanation_score:.2f}")
    print(f"Mean suggestion score: {summary.mean_suggestion_score:.2f}")
    print(f"Mean overall score: {summary.mean_overall_score:.2f}")
    print(f"Mean latency: {summary.mean_latency_ms:.2f}ms")
    
    # Save results
    save_evaluation_results(summary, results)


if __name__ == "__main__":
    asyncio.run(main())

