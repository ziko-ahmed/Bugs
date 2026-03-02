"""
🐛 Easy Bug: Calculator with basic arithmetic errors.

Bug: The subtract function has the operands reversed (b - a instead of a - b).
Bug: The divide function doesn't handle division by zero.
"""


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return b - a  # 🐛 BUG: operands are reversed


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Divide a by b. Raises ValueError on division by zero."""
    return a / b  # 🐛 BUG: no zero check — will raise ZeroDivisionError instead of ValueError
