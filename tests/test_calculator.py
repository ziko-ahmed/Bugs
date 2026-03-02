"""Tests for Easy Bug: Calculator"""

from src.calculator import add, subtract, multiply, divide
import pytest


class TestCalculator:
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0

    def test_subtract(self):
        assert subtract(10, 3) == 7   # Will fail: returns 3 - 10 = -7
        assert subtract(5, 5) == 0
        assert subtract(0, 5) == -5   # Will fail: returns 5 - 0 = 5

    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6

    def test_divide(self):
        assert divide(10, 2) == 5.0
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="division by zero"):
            divide(10, 0)  # Will fail: raises ZeroDivisionError instead of ValueError
