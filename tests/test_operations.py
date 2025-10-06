
import pytest
from app.operation import add, sub, mul, div

@pytest.mark.parametrize("values,expected", [
    ((1, 2, 3), 6.0),
    ((-1, 1, 0.5), 0.5),
    ((10,), 10.0),
])
def test_add(values, expected):
    assert add(*values) == pytest.approx(expected)

@pytest.mark.parametrize("values,expected", [
    ((10, 2, 3), 5.0),
    ((-1, 1), -2.0),
    ((10,), 10.0),
])
def test_sub(values, expected):
    assert sub(*values) == pytest.approx(expected)

@pytest.mark.parametrize("values,expected", [
    ((2, 3, 4), 24.0),
    ((-1, 1), -1.0),
    ((10,), 10.0),
])
def test_mul(values, expected):
    assert mul(*values) == pytest.approx(expected)

@pytest.mark.parametrize("values,expected", [
    ((8, 2, 2), 2.0),
    ((-8, 2), -4.0),
    ((10,), 10.0),
])
def test_div(values, expected):
    assert div(*values) == pytest.approx(expected)

def test_ops_input_validation():
    with pytest.raises(ValueError):
        add("a", 2)
    with pytest.raises(ValueError):
        sub()
    with pytest.raises(ValueError):
        mul()
    with pytest.raises(ValueError):
        div()

def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        div(1, 0)
