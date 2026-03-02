"""Tests for Medium Bug: String utilities"""

from src.string_utils import title_case, truncate, count_vowels, reverse_words


class TestStringUtils:
    def test_title_case_basic(self):
        assert title_case("hello world") == "Hello World"

    def test_title_case_mixed(self):
        assert title_case("hELLO wORLD") == "Hello World"

    def test_truncate_no_truncation(self):
        assert truncate("hello", 10) == "hello"

    def test_truncate_with_suffix(self):
        result = truncate("hello world", 8)
        assert result == "hello..."         # 8 chars total
        assert len(result) <= 8             # Will fail: off-by-one makes it 9

    def test_truncate_custom_suffix(self):
        result = truncate("hello world", 7, suffix="..")
        assert len(result) <= 7             # Will fail: off-by-one

    def test_count_vowels_lowercase(self):
        assert count_vowels("hello") == 2

    def test_count_vowels_mixed_case(self):
        assert count_vowels("Hello World") == 3   # Will fail: misses 'O' uppercase? No — 'e', 'o', 'o'
        # Actually: 'e' in "Hello" + 'o' in "Hello" + 'o' in "World" = 3
        # But 'e' is lowercase so it matches, 'o' lowercase matches
        # Let me make this test clearer:

    def test_count_vowels_uppercase(self):
        assert count_vowels("AEIOU") == 5          # Will fail: all uppercase, none match lowercase vowels

    def test_reverse_words(self):
        assert reverse_words("hello beautiful world") == "world beautiful hello"
