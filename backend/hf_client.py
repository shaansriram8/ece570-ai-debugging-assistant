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
    
    api_url = f"{settings.hf_api_base}/{model_name}"
    headers = {
        "Authorization": f"Bearer {settings.hf_api_key}",
        "Content-Type": "application/json"
    }
    
    model_config = get_model_config(model_name)
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": model_config["temperature"],
            "max_new_tokens": model_config["max_new_tokens"],
            "return_full_text": False
        }
    }
    
    timeout_seconds = timeout or model_config["timeout"]
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            
            latency_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result = response.json()
                # HF API returns different formats, handle common ones
                if isinstance(result, list) and len(result) > 0:
                    if "generated_text" in result[0]:
                        return result[0]["generated_text"], latency_ms, None
                    elif "text" in result[0]:
                        return result[0]["text"], latency_ms, None
                elif isinstance(result, dict):
                    if "generated_text" in result:
                        return result["generated_text"], latency_ms, None
                    elif "text" in result:
                        return result["text"], latency_ms, None
                
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
    lang_context = f"Language: {language}\n" if language else ""
    
    prompt = f"""You are an expert debugging assistant. Analyze the following code and error message, then provide a structured response in JSON format.

{lang_context}Code:
```{language or ''}
{code}
```

Error Message:
```
{error_message}
```

Please provide a JSON response with the following structure:
{{
  "explanation": "A clear, concise explanation of the root cause of this bug",
  "suggestion": "A concrete suggested fix or next debugging steps",
  "score": <number between 0-100 indicating confidence in this explanation>,
  "severity": "low|medium|high" (optional),
  "bug_type": "type of bug, e.g., 'null reference', 'type error', 'logic error'" (optional)
}}

Output ONLY the JSON object, nothing else:"""
    
    return prompt

