"""Caching layer for API responses."""
import hashlib
import json
import time
from typing import Optional, Dict, Any
from config import settings


class ResponseCache:
    """Simple in-memory cache for API responses."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._enabled = settings.cache_enabled
        self._ttl = settings.cache_ttl_seconds
    
    def _generate_key(self, code: str, error_message: str, models: list) -> str:
        """Generate a cache key from code, error message, and model list."""
        content = f"{code}|{error_message}|{','.join(sorted(models))}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get(self, code: str, error_message: str, models: list) -> Optional[Dict[str, Any]]:
        """Retrieve cached response if available and not expired."""
        if not self._enabled:
            return None
        
        key = self._generate_key(code, error_message, models)
        
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        current_time = time.time()
        
        # Check if entry has expired
        if current_time - entry["timestamp"] > self._ttl:
            del self._cache[key]
            return None
        
        return entry["data"]
    
    def set(self, code: str, error_message: str, models: list, data: Dict[str, Any]) -> None:
        """Store response in cache."""
        if not self._enabled:
            return
        
        key = self._generate_key(code, error_message, models)
        self._cache[key] = {
            "data": data,
            "timestamp": time.time()
        }
    
    def clear(self) -> None:
        """Clear all cached entries."""
        self._cache.clear()
    
    def size(self) -> int:
        """Get number of cached entries."""
        return len(self._cache)


# Global cache instance
cache = ResponseCache()

