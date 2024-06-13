import pytest
from functions.functions_maths import addition, subtraction, multiplication, division

def test_addition():
    expected = 7
    result = addition(2, 5)

    assert  result == expected

def test_subtraction():
    expected = 3
    result = subtraction(5, 2)

    assert  result == expected

def test_multiplication():
    expected = 10
    result = multiplication(5, 2)

    assert  result == expected

def test_division_success():
    expected = 5
    result = division(10, 2)

    assert  result == expected

def test_division_by_zero():
    expected = "Zero is not allowed"

    with pytest.raises(ZeroDivisionError) as exception:
        division(10, 0)

    assert str(exception.value) == expected