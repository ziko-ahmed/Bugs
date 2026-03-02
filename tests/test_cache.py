"""Tests for Very Hard Bug: LRU Cache"""

from src.cache import LRUCache


class TestLRUCache:
    def test_basic_put_get(self):
        cache = LRUCache(max_size=3)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.get("a") == 1
        assert cache.get("b") == 2

    def test_cache_miss(self):
        cache = LRUCache(max_size=3)
        assert cache.get("nonexistent") is None
        assert cache.get("nonexistent", "default") == "default"

    def test_eviction_removes_lru(self):
        """
        With max_size=3, after inserting a, b, c, d:
        - 'a' should be evicted (least recently used)
        - 'b', 'c', 'd' should remain
        """
        cache = LRUCache(max_size=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)
        cache.put("d", 4)  # Should evict 'a' (LRU)

        assert cache.get("a") is None    # 'a' was evicted
        assert cache.get("b") == 2
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_access_updates_recency(self):
        """
        After accessing 'a', then inserting 'd',
        'b' should be evicted (now LRU), not 'a'.
        """
        cache = LRUCache(max_size=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)

        # Access 'a' to make it most recently used
        cache.get("a")

        # Insert 'd' — should evict 'b' (least recently used)
        cache.put("d", 4)

        assert cache.get("a") == 1       # Should still be here
        assert cache.get("b") is None    # 'b' was evicted
        assert cache.get("c") == 3
        assert cache.get("d") == 4

    def test_update_existing_key(self):
        cache = LRUCache(max_size=3)
        cache.put("a", 1)
        cache.put("a", 10)
        assert cache.get("a") == 10
        assert cache.size == 1

    def test_delete(self):
        cache = LRUCache(max_size=3)
        cache.put("a", 1)
        assert cache.delete("a") is True
        assert cache.get("a") is None
        assert cache.delete("nonexistent") is False

    def test_hit_rate(self):
        cache = LRUCache(max_size=3)
        cache.put("a", 1)
        cache.get("a")         # hit
        cache.get("b")         # miss
        cache.get("a")         # hit
        assert cache.hit_rate == 2 / 3

    def test_clear(self):
        cache = LRUCache(max_size=3)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.clear()
        assert cache.size == 0
        assert cache.get("a") is None


import pytest
