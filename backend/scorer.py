"""Quality scoring utilities for explanations."""
from typing import Dict, Any, Optional


def compute_heuristic_score(parsed_data: Dict[str, Any]) -> int:
    """
    Compute a quality score based on heuristics (for live system).
    
    Checks:
    - All required fields present
    - Non-empty explanation and suggestion
    - Score is in valid range
    - Presence of optional fields (bonus)
    """
    score = 0
    
    # Required fields (60 points)
    if parsed_data.get("explanation"):
        score += 30
        # Bonus for longer explanations (more detailed)
        if len(parsed_data["explanation"]) > 100:
            score += 10
    
    if parsed_data.get("suggestion"):
        score += 30
        # Bonus for actionable suggestions
        if len(parsed_data["suggestion"]) > 50:
            score += 10
    
    # Score field validity (20 points)
    model_score = parsed_data.get("score", 0)
    if 0 <= model_score <= 100:
        score += 20
    
    # Optional fields (20 points)
    if parsed_data.get("severity"):
        score += 10
    if parsed_data.get("bug_type"):
        score += 10
    
    return min(100, score)


def score_explanation(
    predicted: Dict[str, Any],
    gold: Dict[str, Any]
) -> Dict[str, float]:
    """
    Score predicted explanation against gold/reference explanation.
    
    For evaluation purposes. Compares explanation and suggestion fields using
    word overlap (Jaccard similarity). This is a simple lexical similarity metric.
    
    Note: Semantic similarity (e.g., using sentence-transformers) is not implemented.
    This uses simple word overlap which measures lexical similarity, not semantic similarity.
    
    Args:
        predicted: Predicted response dict
        gold: Gold/reference response dict
    
    Returns:
        Dict with 'explanation_score', 'suggestion_score', 'overall_score' (0-100)
        Scores are based on word overlap: |pred_words ∩ gold_words| / |gold_words|
    """
    scores = {
        "explanation_score": 0.0,
        "suggestion_score": 0.0,
        "overall_score": 0.0
    }
    
    pred_explanation = predicted.get("explanation", "").strip().lower()
    gold_explanation = gold.get("explanation", "").strip().lower()
    
    pred_suggestion = predicted.get("suggestion", "").strip().lower()
    gold_suggestion = gold.get("suggestion", "").strip().lower()
    
    # Word overlap scoring (Jaccard similarity - lexical, not semantic)
    # Explanation scoring (simple word overlap)
    if gold_explanation:
        pred_words = set(pred_explanation.split())
        gold_words = set(gold_explanation.split())
        if gold_words:
            overlap = len(pred_words & gold_words) / len(gold_words)
            scores["explanation_score"] = overlap * 100
    
    # Suggestion scoring
    if gold_suggestion:
        pred_words = set(pred_suggestion.split())
        gold_words = set(gold_suggestion.split())
        if gold_words:
            overlap = len(pred_words & gold_words) / len(gold_words)
            scores["suggestion_score"] = overlap * 100
    
    # Overall score (average)
    scores["overall_score"] = (scores["explanation_score"] + scores["suggestion_score"]) / 2
    
    return scores

