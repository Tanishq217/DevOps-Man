import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.calculator import add, subtract, multiply, divide, calculate


def test_add():
    assert add(10, 5) == 15
    assert add(-3, 3) == 0
    assert add(2.5, 3.5) == 6.0


def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(5, 10) == -5
    assert subtract(0, 7) == -7


def test_multiply():
    assert multiply(10, 5) == 50
    assert multiply(-4, 3) == -12
    assert multiply(0, 100) == 0


def test_divide():
    assert divide(10, 5) == 2.0
    assert divide(9, 2) == 4.5
    assert divide(-12, 3) == -4.0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)


def test_calculate_dispatcher():
    assert calculate(8, '+', 2) == 10
    assert calculate(8, '-', 2) == 6
    assert calculate(8, '*', 2) == 16
    assert calculate(8, '/', 2) == 4
    with pytest.raises(ValueError, match="Unsupported operator"):
        calculate(8, '%', 2)
