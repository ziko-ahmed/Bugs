"""Tests for String utilities"""

from src.string_utils import title_case, truncate, count_vowels, reverse_words


class TestStringUtils:
    def test_title_case_basic(self):
        assert title_case("hello world") == "Hello World"

    def test_title_case_mixed(self):
        assert title_case("hELLO wORLD") == "Hello World"

    def test_title_case_empty(self):
        assert title_case("") == ""

    def test_title_case_none(self):
        assert title_case(None) == ""

    def test_truncate_no_truncation(self):
        assert truncate("hello", 10) == "hello"

    def test_truncate_with_suffix(self):
        result = truncate("hello world", 8)
        assert result == "hello..."         # 8 chars total
        assert len(result) <= 8             # Will pass: off-by-one fixed

    def test_truncate_custom_suffix(self):
        result = truncate("hello world", 7, suffix="..")
        assert len(result) <= 7             # Will pass: off-by-one fixed

    def test_count_vowels_lowercase(self):
        assert count_vowels("hello") == 2

    def test_count_vowels_mixed_case(self):
        assert count_vowels("Hello World") == 3  

    def test_count_vowels_uppercase(self):
        assert count_vowels("AEIOU") == 5          # Will pass: uppercase vowels matched

    def test_reverse_words(self):
        assert reverse_words("hello beautiful world") == "world beautiful hello"
