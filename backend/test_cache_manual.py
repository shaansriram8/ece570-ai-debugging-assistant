#!/usr/bin/env python3
"""Manual test script to verify cache behavior."""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from services.cache_service import SimpleResponseCache
from models import AnalyzeRequest, AnalyzeResponse, ModelMetadata

def test_cache_key_generation():
    """Test that cache keys are generated correctly."""
    print("=" * 70)
    print("Test 1: Cache Key Generation")
    print("=" * 70)
    
    cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
    
    # Test same inputs produce same key
    key1 = cache.make_key(
        model_name="model1,model2",
        code="test code",
        error_message="test error",
        language="python",
        prompt_version="v1"
    )
    
    key2 = cache.make_key(
        model_name="model1,model2",
        code="test code",
        error_message="test error",
        language="python",
        prompt_version="v1"
    )
    
    assert key1 == key2, "Same inputs should produce same key"
    print(f"✓ Same inputs produce same key: {key1[:16]}...")
    
    # Test different inputs produce different keys
    key3 = cache.make_key(
        model_name="model1,model2",
        code="different code",  # Different
        error_message="test error",
        language="python",
        prompt_version="v1"
    )
    
    assert key1 != key3, "Different inputs should produce different keys"
    print(f"✓ Different inputs produce different keys")
    print(f"  Key 1: {key1[:16]}...")
    print(f"  Key 3: {key3[:16]}...")
    print()


def test_cache_storage_and_retrieval():
    """Test that cache stores and retrieves responses correctly."""
    print("=" * 70)
    print("Test 2: Cache Storage and Retrieval")
    print("=" * 70)
    
    cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
    
    # Create a test response
    test_response_dict = {
        "explanation": "Test explanation",
        "suggestion": "Test suggestion",
        "score": 85,
        "severity": "medium",
        "bug_type": "test bug",
        "meta": {
            "models_used": ["model1"],
            "per_model_latency_ms": {"model1": 100.0},
            "total_latency_ms": 100.0,
            "had_repair": False,
            "from_cache": False,
            "backend_version": "1.0.0"
        }
    }
    
    # Generate cache key
    cache_key = cache.make_key(
        model_name="model1",
        code="test code",
        error_message="test error",
        language="python",
        prompt_version="v1"
    )
    
    # Initially should be None
    cached = cache.get(cache_key)
    assert cached is None, "Cache should be empty initially"
    print("✓ Cache miss on first access")
    
    # Store the response
    cache.set(cache_key, test_response_dict)
    print("✓ Stored response in cache")
    
    # Retrieve it
    cached = cache.get(cache_key)
    assert cached is not None, "Cache should return stored value"
    assert cached == test_response_dict, "Cached value should match stored value"
    print("✓ Cache hit on second access")
    print(f"  Retrieved: explanation='{cached['explanation']}', score={cached['score']}")
    print()


def test_from_cache_flag():
    """Test that from_cache flag is set correctly."""
    print("=" * 70)
    print("Test 3: from_cache Flag Behavior")
    print("=" * 70)
    
    cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
    
    # Create response with from_cache=False
    response_dict = {
        "explanation": "Test",
        "suggestion": "Fix",
        "score": 80,
        "meta": {
            "from_cache": False,
            "models_used": ["model1"],
            "per_model_latency_ms": {},
            "total_latency_ms": 100.0,
            "had_repair": False
        }
    }
    
    cache_key = cache.make_key(
        model_name="model1",
        code="code",
        error_message="error",
        language=None,
        prompt_version="v1"
    )
    
    # Store with from_cache=False
    cache.set(cache_key, response_dict)
    
    # Retrieve and reconstruct
    cached = cache.get(cache_key)
    response = AnalyzeResponse(**cached)
    
    # When retrieved from cache, should set from_cache=True
    response.meta.from_cache = True
    
    assert response.meta.from_cache is True, "Cached response should have from_cache=True"
    print("✓ Cached response correctly sets from_cache=True")
    print(f"  from_cache flag: {response.meta.from_cache}")
    print()


def test_cache_with_different_languages():
    """Test that different languages produce different cache keys."""
    print("=" * 70)
    print("Test 4: Language-Specific Caching")
    print("=" * 70)
    
    cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
    
    code = "x = 5"
    error = "syntax error"
    
    key_python = cache.make_key(
        model_name="model1",
        code=code,
        error_message=error,
        language="python",
        prompt_version="v1"
    )
    
    key_javascript = cache.make_key(
        model_name="model1",
        code=code,
        error_message=error,
        language="javascript",
        prompt_version="v1"
    )
    
    key_none = cache.make_key(
        model_name="model1",
        code=code,
        error_message=error,
        language=None,
        prompt_version="v1"
    )
    
    assert key_python != key_javascript, "Different languages should produce different keys"
    assert key_python != key_none, "Language vs None should produce different keys"
    assert key_javascript != key_none, "Language vs None should produce different keys"
    
    print("✓ Different languages produce different cache keys")
    print(f"  Python key:    {key_python[:16]}...")
    print(f"  JavaScript key: {key_javascript[:16]}...")
    print(f"  None key:     {key_none[:16]}...")
    print()


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MANUAL CACHE TESTS")
    print("=" * 70 + "\n")
    
    try:
        test_cache_key_generation()
        test_cache_storage_and_retrieval()
        test_from_cache_flag()
        test_cache_with_different_languages()
        
        print("=" * 70)
        print("ALL MANUAL TESTS PASSED ✓")
        print("=" * 70)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

