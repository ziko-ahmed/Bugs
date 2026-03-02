"""
String utilities with edge-case handling.

Functions:
    title_case: Convert text to title case.
    truncate: Truncate text to max_length, adding suffix if truncated.
    count_vowels: Count all vowels (case-insensitive) in the text.
    reverse_words: Reverse the order of words in a string.
"""


def title_case(text: str) -> str:
    """Convert text to title case. Returns empty string for empty input."""
    if text is None:
        return ""
    words = text.split()
    return " ".join(w[0].upper() + w[1:].lower() if w else "" for w in words)


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, adding suffix if truncated."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def count_vowels(text: str) -> int:
    """Count all vowels (case-insensitive) in the text."""
    vowels = "aeiouAEIOU"
    return sum(1 for c in text if c in vowels)


def reverse_words(text: str) -> str:
    """Reverse the order of words in a string."""
    return " ".join(text.split()[::-1])
