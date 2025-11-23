"""JSON extraction, repair, and validation utilities."""
import json
import re
from typing import Dict, Any, Optional, Tuple


def extract_json_from_text(text: str) -> Optional[str]:
    """
    Extract the first JSON object block from free-form text.
    
    Uses regex to find the first { ... } block that looks like JSON.
    """
    # Pattern to match JSON object: { ... }
    # Handles nested braces by matching balanced pairs
    pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    
    matches = re.findall(pattern, text, re.DOTALL)
    
    if not matches:
        return None
    
    # Return the first (longest) match
    return max(matches, key=len)


def repair_json(json_str: str) -> Optional[str]:
    """
    Attempt to repair common JSON syntax issues.
    
    Handles:
    - Trailing commas
    - Single quotes instead of double quotes
    - Missing quotes around keys
    - Comments (removes them)
    """
    try:
        # Try parsing first - if it works, no repair needed
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError:
        pass
    
    # Remove comments (both // and /* */ style)
    json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
    json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
    
    # Replace single quotes with double quotes (but be careful with strings)
    # This is a simple approach - may not handle all edge cases
    json_str = re.sub(r"'([^']*)':", r'"\1":', json_str)
    json_str = re.sub(r":\s*'([^']*)'", r': "\1"', json_str)
    
    # Remove trailing commas before } or ]
    json_str = re.sub(r',\s*}', '}', json_str)
    json_str = re.sub(r',\s*]', ']', json_str)
    
    # Try to add missing quotes around unquoted keys
    json_str = re.sub(r'(\w+):', r'"\1":', json_str)
    
    try:
        # Validate the repaired JSON
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError:
        return None


def normalize_json_schema(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize and validate JSON schema to ensure required fields exist.
    
    Ensures the response has the expected structure with defaults for missing fields.
    """
    normalized = {
        "explanation": data.get("explanation", ""),
        "suggestion": data.get("suggestion", ""),
        "score": data.get("score", 0),
    }
    
    # Optional fields
    if "severity" in data:
        normalized["severity"] = data["severity"]
    if "bug_type" in data:
        normalized["bug_type"] = data["bug_type"]
    
    # Ensure score is in valid range
    normalized["score"] = max(0, min(100, int(normalized["score"])))
    
    return normalized


def parse_model_output(text: str) -> Tuple[Optional[Dict[str, Any]], bool]:
    """
    Parse model output text into structured JSON.
    
    Returns:
        (parsed_data, had_repair) - parsed JSON dict or None, and whether repair was used
    """
    # Step 1: Extract JSON block
    json_str = extract_json_from_text(text)
    
    if json_str is None:
        # Log first 500 chars for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to extract JSON from model output. First 500 chars: {text[:500]}")
        return None, False
    
    # Step 2: Try to parse
    try:
        data = json.loads(json_str)
        normalized = normalize_json_schema(data)
        return normalized, False
    except json.JSONDecodeError:
        pass
    
    # Step 3: Attempt repair
    repaired = repair_json(json_str)
    if repaired is None:
        return None, False
    
    try:
        data = json.loads(repaired)
        normalized = normalize_json_schema(data)
        return normalized, True
    except json.JSONDecodeError:
        return None, False

