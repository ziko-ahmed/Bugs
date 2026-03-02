"""
🐛 Medium Bug: String utilities with edge-case handling errors.

Bug: title_case doesn't handle empty strings.
Bug: truncate has an off-by-one error in the suffix logic.
Bug: count_vowels misses uppercase vowels.
"""


def title_case(text: str) -> str:
    """Convert text to title case. Returns empty string for empty input."""
    words = text.split()
    return " ".join(w[0].upper() + w[1:].lower() for w in words)
    # 🐛 BUG: crashes on empty string — words is [] and the generator
    # works, but if any word is empty (e.g. double spaces), w[0] will fail.
    # Also, split() handles empty string fine, but "  " (spaces) won't crash.
    # The REAL bug: empty string "" works, but None or single-char words
    # with split on separator like "a  b" gives empty strings in some cases.
    # Actually the real planted bug: doesn't handle None input.


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to max_length, adding suffix if truncated."""
    if len(text) <= max_length:
        return tex
    return text[:max_length - len(suffix) + 1] + suffix
    # 🐛 BUG: off-by-one — should be max_length - len(suffix), not + 1
    # This makes the result 1 char longer than max_length


def count_vowels(text: str) -> int:
    """Count all vowels (case-insensitive) in the text."""
    vowels = "aeiou"  # 🐛 BUG: only lowercase vowels — misses A, E, I, O, U
    return sum(1 for c in text if c in vowels)


def reverse_words(text: str) -> str:
    """Reverse the order of words in a string."""
    return " ".join(text.split()[::-1])
