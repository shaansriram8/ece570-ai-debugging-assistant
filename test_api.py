#!/usr/bin/env python3
"""
Simple script to test the backend API without using the UI.
Shows the structured JSON output directly.
"""
import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("=" * 70)
    print("Testing /health endpoint")
    print("=" * 70)
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print("\nResponse JSON:")
    print(json.dumps(response.json(), indent=2))
    print()

def test_analyze(code, error_message, language=None):
    """Test the /analyze endpoint."""
    print("=" * 70)
    print("Testing /analyze endpoint")
    print("=" * 70)
    
    payload = {
        "code": code,
        "error_message": error_message
    }
    
    if language:
        payload["language"] = language
    
    print(f"\nRequest Payload:")
    print(json.dumps(payload, indent=2))
    print("\nSending request...")
    
    response = requests.post(
        f"{API_BASE_URL}/analyze",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "=" * 70)
        print("FULL RESPONSE JSON:")
        print("=" * 70)
        print(json.dumps(result, indent=2))
        
        print("\n" + "=" * 70)
        print("FORMATTED OUTPUT:")
        print("=" * 70)
        print(f"\nExplanation:\n{result['explanation']}")
        print(f"\nSuggestion:\n{result['suggestion']}")
        print(f"\nScore: {result['score']}/100")
        print(f"Severity: {result.get('severity', 'N/A')}")
        print(f"Bug Type: {result.get('bug_type', 'N/A')}")
        
        print("\n" + "-" * 70)
        print("METADATA:")
        print("-" * 70)
        meta = result['meta']
        print(f"Models Used: {', '.join(meta['models_used'])}")
        print(f"Total Latency: {meta['total_latency_ms']:.2f}ms")
        print(f"From Cache: {meta['from_cache']}")
        print(f"Had Repair: {meta['had_repair']}")
        print("\nPer-Model Latency:")
        for model, latency in meta['per_model_latency_ms'].items():
            print(f"  - {model}: {latency:.2f}ms")
    else:
        print(f"\nError: {response.text}")

if __name__ == "__main__":
    # Test 1: Health check
    try:
        test_health()
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to backend. Is it running on http://localhost:8000?")
        sys.exit(1)
    
    # Test 2: JavaScript analysis
    print("\n\n")
    test_analyze(
        code='const x = "hello";\nconst y = x.length();',
        error_message='TypeError: x.length is not a function',
        language='javascript'
    )
    
    # Test 3: JavaScript undefined error
    print("\n\n")
    test_analyze(
        code='const arr = undefined;\nconst result = arr.map(x => x * 2);',
        error_message='TypeError: Cannot read property \'map\' of undefined',
        language='javascript'
    )
    
    # Test 4: Python example
    print("\n\n")
    test_analyze(
        code='def divide(a, b):\n    return a / b\n\nresult = divide(10, 0)',
        error_message='ZeroDivisionError: division by zero',
        language='python'
    )

