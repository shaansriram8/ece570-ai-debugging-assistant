"""Response aggregation logic for multi-model outputs."""
from typing import Dict, Any, List, Optional, Tuple
from json_handler import parse_model_output


def aggregate_responses(
    model_responses: Dict[str, Tuple[Optional[str], float, Optional[str]]],
    model_parsed: Dict[str, Tuple[Optional[Dict[str, Any]], bool]]
) -> Dict[str, Any]:
    """
    Aggregate multiple model responses into a single unified response.
    
    Strategy:
    1. Prefer primary model if it has valid JSON
    2. If primary fails, use secondary model
    3. If multiple valid, combine explanations and take average score
    4. Use majority vote for severity/bug_type if available
    
    Args:
        model_responses: Dict mapping model_name -> (text, latency_ms, error)
        model_parsed: Dict mapping model_name -> (parsed_json, had_repair)
    
    Returns:
        Aggregated response dictionary with explanation, suggestion, score, etc.
    """
    valid_responses = []
    
    # Collect all valid parsed responses
    for model_name, (parsed_data, had_repair) in model_parsed.items():
        if parsed_data is not None:
            text, latency, error = model_responses.get(model_name, (None, 0.0, None))
            valid_responses.append({
                "model": model_name,
                "data": parsed_data,
                "latency": latency,
                "had_repair": had_repair
            })
    
    if not valid_responses:
        # No valid responses - return default/error response
        return {
            "explanation": "Unable to analyze the code. All models failed to produce valid responses.",
            "suggestion": "Please check your code and error message, and try again.",
            "score": 0,
            "severity": None,
            "bug_type": None
        }
    
    # If only one valid response, use it directly
    if len(valid_responses) == 1:
        result = valid_responses[0]["data"].copy()
        return result
    
    # Multiple valid responses - aggregate
    # Strategy: Use primary model's explanation/suggestion, average the scores
    primary = valid_responses[0]
    aggregated = primary["data"].copy()
    
    # Average the scores
    scores = [r["data"].get("score", 0) for r in valid_responses]
    aggregated["score"] = int(sum(scores) / len(scores))
    
    # If primary had repair but another didn't, prefer the non-repaired one
    non_repaired = [r for r in valid_responses if not r["had_repair"]]
    if non_repaired:
        aggregated = non_repaired[0]["data"].copy()
        aggregated["score"] = int(sum(scores) / len(scores))
    
    # Majority vote for severity and bug_type
    severities = [r["data"].get("severity") for r in valid_responses if r["data"].get("severity")]
    if severities:
        # Simple majority vote
        from collections import Counter
        severity_counts = Counter(severities)
        aggregated["severity"] = severity_counts.most_common(1)[0][0]
    
    bug_types = [r["data"].get("bug_type") for r in valid_responses if r["data"].get("bug_type")]
    if bug_types:
        from collections import Counter
        bug_type_counts = Counter(bug_types)
        aggregated["bug_type"] = bug_type_counts.most_common(1)[0][0]
    
    return aggregated


def process_model_outputs(
    model_responses: Dict[str, Tuple[Optional[str], float, Optional[str]]]
) -> Tuple[Dict[str, Tuple[Optional[Dict[str, Any]], bool]], Dict[str, Any]]:
    """
    Parse all model outputs and aggregate them.
    
    Returns:
        (model_parsed, aggregated_response)
        - model_parsed: Dict mapping model_name -> (parsed_json, had_repair)
        - aggregated_response: Final aggregated response dict
    """
    model_parsed = {}
    
    # Parse each model's output
    for model_name, (text, latency, error) in model_responses.items():
        if text is None:
            model_parsed[model_name] = (None, False)
        else:
            parsed, had_repair = parse_model_output(text)
            model_parsed[model_name] = (parsed, had_repair)
    
    # Aggregate responses
    aggregated = aggregate_responses(model_responses, model_parsed)
    
    return model_parsed, aggregated

