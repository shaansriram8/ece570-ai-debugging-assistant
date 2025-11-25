"""Response cache service for exact-response caching."""
import time
import hashlib
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    """Cache entry with value, creation time, and TTL."""
    value: Any
    created_at: float
    ttl_seconds: int

    def is_expired(self) -> bool:
        """Check if the cache entry has expired."""
        return (time.time() - self.created_at) > self.ttl_seconds


class SimpleResponseCache:
    """Simple in-memory cache with TTL and size-based eviction."""
    
    def __init__(self, max_size: int, default_ttl_seconds: int):
        """
        Initialize the cache.
        
        Args:
            max_size: Maximum number of entries before eviction
            default_ttl_seconds: Default TTL for cache entries
        """
        self._store: Dict[str, CacheEntry] = {}
        self._max_size = max_size
        self._default_ttl = default_ttl_seconds

    def _evict_if_needed(self) -> None:
        """Evict oldest entry if cache exceeds max_size."""
        if len(self._store) <= self._max_size:
            return
        # Simple eviction: drop oldest entry
        if self._store:
            oldest_key = min(self._store.items(), key=lambda kv: kv[1].created_at)[0]
            self._store.pop(oldest_key, None)

    def make_key(
        self,
        *,
        model_name: str,
        code: str,
        error_message: str,
        language: Optional[str],
        prompt_version: str
    ) -> str:
        """
        Generate a cache key from the logical inputs.
        
        Args:
            model_name: Model name or sorted comma-separated list of models
            code: Source code
            error_message: Error message
            language: Programming language (optional)
            prompt_version: Prompt template version
            
        Returns:
            SHA256 hash of the concatenated inputs
        """
        raw = "|".join([
            model_name,
            language or "",
            prompt_version,
            code,
            error_message,
        ])
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found and not expired, None otherwise
        """
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.is_expired():
            self._store.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        Store a value in the cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Optional TTL override (uses default if not provided)
        """
        ttl = ttl_seconds or self._default_ttl
        self._store[key] = CacheEntry(
            value=value,
            created_at=time.time(),
            ttl_seconds=ttl
        )
        self._evict_if_needed()

    def clear(self) -> None:
        """Clear all cache entries."""
        self._store.clear()

    def size(self) -> int:
        """Get current number of cache entries."""
        return len(self._store)


# Import config at module level to avoid circular imports
# We'll import the specific values we need
try:
    from config import settings
    response_cache = SimpleResponseCache(
        max_size=settings.cache_max_size,
        default_ttl_seconds=settings.cache_default_ttl_seconds,
    )
except ImportError:
    # Fallback for testing or if config isn't available
    response_cache = SimpleResponseCache(
        max_size=512,
        default_ttl_seconds=3600,
    )

