import unittest
from src.calculator import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(10, 3), 13)

    def test_subtract(self):
        self.assertEqual(subtract(10, 3), 7)

    def test_multiply(self):
        self.assertEqual(multiply(10, 3), 30)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
