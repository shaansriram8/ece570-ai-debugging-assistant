"""Hugging Face Inference API client."""
import asyncio
import time
from typing import Dict, Any, Optional, List, Tuple
import httpx
from config import settings, get_model_config


async def call_hf_model(
    model_name: str,
    prompt: str,
    timeout: Optional[int] = None
) -> Tuple[Optional[str], float, Optional[str]]:
    """
    Call Hugging Face Inference API for a single model.
    
    Args:
        model_name: Name of the model (e.g., "01-ai/Yi-1.5B-Coder")
        prompt: Input prompt text
        timeout: Request timeout in seconds (defaults to config timeout)
    
    Returns:
        (response_text, latency_ms, error_message)
        - response_text: Model output text, or None if error
        - latency_ms: Request latency in milliseconds
        - error_message: Error description if failed, None if success
    """
    if not settings.hf_api_key:
        return None, 0.0, "HF_API_KEY not configured"
    
    # New router API uses OpenAI-compatible chat completions endpoint
    api_url = settings.hf_api_base  # Already includes full path: https://router.huggingface.co/v1/chat/completions
    headers = {
        "Authorization": f"Bearer {settings.hf_api_key}",
        "Content-Type": "application/json"
    }
    
    model_config = get_model_config(model_name)
    
    # New format: OpenAI-compatible chat completions
    # Use system message for better context and technical accuracy
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert software debugging assistant specializing in code error analysis. You provide technically accurate, precise explanations of code bugs. CRITICAL: Always pay attention to the programming language specified in the user's request - use language-specific syntax, conventions, and terminology. Do NOT confuse languages (e.g., Java vs C++, JavaScript vs TypeScript). Only report actual bugs - do NOT invent errors when code is correct. Always use correct terminology (e.g., properties vs methods, types, etc.) and ensure your technical facts are correct. Focus on accuracy and clarity."
            },
            {"role": "user", "content": prompt}
        ],
        "max_tokens": model_config["max_new_tokens"],
        "temperature": model_config["temperature"]
    }
    
    timeout_seconds = timeout or model_config["timeout"]
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            
            latency_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                # New format: {"choices": [{"message": {"content": "..."}}]}
                if isinstance(result, dict) and "choices" in result:
                    if len(result["choices"]) > 0:
                        content = result["choices"][0].get("message", {}).get("content", "")
                        if content:
                            return content, latency_ms, None
                
                # Fallback: try to extract text from response
                return str(result), latency_ms, None
            else:
                error_msg = f"API error {response.status_code}: {response.text}"
                return None, latency_ms, error_msg
                
    except httpx.TimeoutException:
        latency_ms = (time.time() - start_time) * 1000
        return None, latency_ms, f"Request timeout after {timeout_seconds}s"
    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        return None, latency_ms, f"Request failed: {str(e)}"


async def call_multiple_models(
    prompt: str,
    model_names: List[str]
) -> Dict[str, Tuple[Optional[str], float, Optional[str]]]:
    """
    Call multiple models in parallel.
    
    Args:
        prompt: Input prompt text
        model_names: List of model names to call
    
    Returns:
        Dictionary mapping model_name -> (response_text, latency_ms, error_message)
    """
    tasks = [
        call_hf_model(model_name, prompt)
        for model_name in model_names
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    output = {}
    for model_name, result in zip(model_names, results):
        if isinstance(result, Exception):
            output[model_name] = (None, 0.0, f"Exception: {str(result)}")
        else:
            output[model_name] = result
    
    return output


def build_analysis_prompt(code: str, error_message: str, language: Optional[str] = None) -> str:
    """
    Build a prompt for the LLM to analyze code and error.
    
    Returns a structured prompt that instructs the model to output JSON.
    """
    # Strongly emphasize the programming language
    if language:
        lang_context = f"IMPORTANT: The code is written in {language.upper()}. Use {language}-specific syntax, conventions, and terminology. Do NOT confuse it with other languages.\n\n"
    else:
        lang_context = ""
    
    # Handle "N/A" or empty error messages
    if error_message.upper() in ["N/A", "NA", "NONE", ""]:
        error_context = "No error message provided. Only analyze if there is an actual bug in the code. If the code is correct and has no errors, state that clearly."
    else:
        error_context = f"Error Message:\n```\n{error_message}\n```"
    
    prompt = f"""You are an expert debugging assistant with deep technical knowledge. Analyze the following code and error message with technical precision and accuracy.

CRITICAL REQUIREMENTS:
- Be technically accurate: Use correct terminology (properties vs methods, types, etc.)
- Explain the root cause precisely: What exactly is wrong and why
- Provide actionable fixes: Concrete code changes or debugging steps
- Verify technical facts: Ensure your explanation is factually correct
- If the code is correct and has no errors, state that clearly - do NOT invent errors
- For syntax errors: Check for missing semicolons, brackets, parentheses, quotes, etc.
- For Java: Statements must end with semicolons. Variable declarations like 'int x = 5' need a semicolon: 'int x = 5;'

{lang_context}Code:
```{language or ''}
{code}
```

{error_context}

TECHNICAL GUIDANCE:
- Pay attention to the programming language specified above - use language-specific syntax and conventions
- CHECK SYNTAX FIRST: Look for missing semicolons, brackets, parentheses, quotes, etc.
- For Java: All statements must end with semicolons (;). Missing semicolon is a syntax error.
- For "is not a function" errors: Distinguish between properties and methods correctly
- For "undefined/null" errors: Explain the null/undefined state and why it occurred
- For type errors: Explain the type mismatch precisely
- For logic errors: Explain the incorrect logic flow
- If no error message is provided, only report actual bugs in the code - do not invent problems
- Severity: "high" = crashes/breaks execution, "medium" = incorrect behavior, "low" = minor issues

Provide a JSON response with the following structure:
{{
  "explanation": "A technically accurate, precise explanation of the root cause. Use correct terminology and be factually correct.",
  "suggestion": "A concrete, actionable fix with specific code changes or debugging steps",
  "score": <number between 0-100 indicating confidence in this explanation>,
  "severity": "low|medium|high" (optional, based on impact: high=crashes, medium=wrong behavior, low=minor),
  "bug_type": "type of bug, e.g., 'null reference', 'type error', 'logic error', 'syntax error'" (optional)
}}

Output ONLY the JSON object, nothing else. Ensure all technical details are accurate:"""
    
    return prompt

