"""
🐛 Very Hard Bug: LRU Cache with subtle concurrency and eviction bugs.

Bug: Cache eviction removes the WRONG item (most recently used instead of least).
Bug: The access order tracking is broken — get() doesn't update recency.
Bug: max_size=0 should disable caching but instead causes KeyError.
"""

from collections import OrderedDict
from typing import Any


class LRUCache:
    """Least Recently Used cache with a maximum size."""

    def __init__(self, max_size: int = 128):
        self.max_size = max_size
        self._cache: OrderedDict[str, Any] = OrderedDict()
        self._hits = 0
        self._misses = 0

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the cache. Moves it to most-recent position.
        Returns default if key not found.
        """
        if key not in self._cache:
            self._misses += 1
            return default

        self._hits += 1
        # 🐛 BUG: should call move_to_end(key, last=True) to mark as recently used
        # Without this, the access order is never updated, so "LRU" eviction
        # is actually "insertion order" eviction — evicts oldest INSERT, not oldest ACCESS
        return self._cache[key]

    def put(self, key: str, value: Any) -> None:
        """Add or update a key-value pair in the cache."""
        if key in self._cache:
            self._cache[key] = value
            self._cache.move_to_end(key, last=True)
            return

        if len(self._cache) >= self.max_size:
            # 🐛 BUG: last=True removes the MOST recently used item!
            # Should be last=False to remove the LEAST recently used item
            self._cache.popitem(last=True)

        self._cache[key] = value

    def delete(self, key: str) -> bool:
        """Remove a key from the cache. Returns True if key existed."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        """Clear the entire cache."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    @property
    def size(self) -> int:
        return len(self._cache)

    @property
    def hit_rate(self) -> float:
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return self._hits / total

    def __contains__(self, key: str) -> bool:
        return key in self._cache

    def __repr__(self) -> str:
        return f"LRUCache(size={self.size}/{self.max_size}, hit_rate={self.hit_rate:.2%})"
