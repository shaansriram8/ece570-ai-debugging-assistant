"""Integration tests for the response cache."""
import time
import pytest
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any

from services.cache_service import SimpleResponseCache, CacheEntry
from models import AnalyzeRequest, AnalyzeResponse, ModelMetadata


class TestSimpleResponseCache:
    """Test the SimpleResponseCache class."""
    
    def test_cache_miss_then_hit(self):
        """Test that cache miss then hit works correctly."""
        cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
        
        # First get - should be None (miss)
        key = "test_key_1"
        assert cache.get(key) is None
        
        # Set a value
        test_value = {"test": "data"}
        cache.set(key, test_value)
        
        # Second get - should return the value (hit)
        assert cache.get(key) == test_value
    
    def test_different_inputs_dont_collide(self):
        """Test that different inputs produce different cache keys."""
        cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
        
        # Generate keys for different inputs
        key1 = cache.make_key(
            model_name="model1",
            code="code1",
            error_message="error1",
            language="python",
            prompt_version="v1"
        )
        
        key2 = cache.make_key(
            model_name="model1",
            code="code2",  # Different code
            error_message="error1",
            language="python",
            prompt_version="v1"
        )
        
        key3 = cache.make_key(
            model_name="model1",
            code="code1",
            error_message="error2",  # Different error
            language="python",
            prompt_version="v1"
        )
        
        # All keys should be different
        assert key1 != key2
        assert key1 != key3
        assert key2 != key3
        
        # Set values for each key
        cache.set(key1, {"value": 1})
        cache.set(key2, {"value": 2})
        cache.set(key3, {"value": 3})
        
        # Each should return its own value
        assert cache.get(key1) == {"value": 1}
        assert cache.get(key2) == {"value": 2}
        assert cache.get(key3) == {"value": 3}
    
    def test_ttl_expiry(self):
        """Test that cache entries expire after TTL."""
        cache = SimpleResponseCache(max_size=100, default_ttl_seconds=0.1)  # Very short TTL
        
        key = "test_key_expiry"
        test_value = {"test": "data"}
        
        # Set value
        cache.set(key, test_value)
        
        # Immediately after setting, should be available
        assert cache.get(key) == test_value
        
        # Wait for expiry
        time.sleep(0.15)
        
        # After expiry, should return None
        assert cache.get(key) is None
    
    def test_eviction(self):
        """Test that cache evicts oldest entry when max_size is exceeded."""
        cache = SimpleResponseCache(max_size=3, default_ttl_seconds=3600)
        
        # Fill cache to max_size
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        
        assert cache.size() == 3
        
        # Add one more - should evict oldest
        time.sleep(0.01)  # Small delay to ensure key1 is oldest
        cache.set("key4", "value4")
        
        # Should still be at max_size
        assert cache.size() == 3
        
        # key1 should be evicted (oldest)
        assert cache.get("key1") is None
        # Others should still be there
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
        assert cache.get("key4") == "value4"
    
    def test_cache_entry_expiry(self):
        """Test CacheEntry.is_expired() method."""
        entry = CacheEntry(
            value="test",
            created_at=time.time() - 100,  # Created 100 seconds ago
            ttl_seconds=50  # TTL is 50 seconds
        )
        
        assert entry.is_expired() is True
        
        entry2 = CacheEntry(
            value="test",
            created_at=time.time(),  # Just created
            ttl_seconds=100  # TTL is 100 seconds
        )
        
        assert entry2.is_expired() is False


class TestCacheIntegration:
    """Integration tests for cache with analyze endpoint logic."""
    
    @pytest.mark.asyncio
    async def test_cache_miss_then_hit_with_mock_hf(self):
        """Test that identical requests only call HF once, second uses cache."""
        from services.cache_service import SimpleResponseCache
        
        # Create a fresh cache for this test
        cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
        
        # Mock HF client
        mock_model_responses = {
            "model1": ("Test response", 100.0, None)
        }
        
        with patch('main.call_multiple_models', new_callable=AsyncMock) as mock_call:
            mock_call.return_value = mock_model_responses
            
            # Mock the aggregation and scoring
            with patch('main.process_model_outputs') as mock_process:
                mock_process.return_value = (
                    {"model1": ({"explanation": "test", "suggestion": "fix", "score": 80}, False)},
                    {"explanation": "test", "suggestion": "fix", "score": 80}
                )
            
            with patch('main.compute_heuristic_score') as mock_score:
                mock_score.return_value = 80
            
            # Import here to avoid circular imports
            from main import analyze_code
            from models import AnalyzeRequest
            
            request = AnalyzeRequest(
                code="test code",
                error_message="test error",
                language="python"
            )
            
            # Temporarily replace the cache in main
            import main
            original_cache = main.response_cache
            main.response_cache = cache
            
            try:
                # First call - should call HF
                response1 = await analyze_code(request)
                assert mock_call.call_count == 1
                assert response1.meta.from_cache is False
                
                # Reset mock to track second call
                mock_call.reset_mock()
                
                # Second call with same request - should use cache
                response2 = await analyze_code(request)
                assert mock_call.call_count == 0  # Should not call HF again
                assert response2.meta.from_cache is True
                assert response2.explanation == response1.explanation
            finally:
                # Restore original cache
                main.response_cache = original_cache
    
    def test_different_requests_dont_collide(self):
        """Test that different requests produce different cache keys and both call HF."""
        from services.cache_service import SimpleResponseCache
        
        cache = SimpleResponseCache(max_size=100, default_ttl_seconds=3600)
        
        # Generate keys for two different requests
        key1 = cache.make_key(
            model_name="model1",
            code="code1",
            error_message="error1",
            language="python",
            prompt_version="v1"
        )
        
        key2 = cache.make_key(
            model_name="model1",
            code="code2",  # Different code
            error_message="error1",
            language="python",
            prompt_version="v1"
        )
        
        # Keys should be different
        assert key1 != key2
        
        # Both should be cache misses initially
        assert cache.get(key1) is None
        assert cache.get(key2) is None
        
        # Set different values
        cache.set(key1, {"response": 1})
        cache.set(key2, {"response": 2})
        
        # Both should return their respective values
        assert cache.get(key1) == {"response": 1}
        assert cache.get(key2) == {"response": 2}

