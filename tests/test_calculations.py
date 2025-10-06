
import pytest
from app.calculation.calculation import Calculation, History
from app.calculation.factory import create_calculation, OPERATIONS

def test_create_calculation_and_compute():
    calc = create_calculation("add", 1, 2, 3)
    assert isinstance(calc, Calculation)
    assert calc.compute() == 6.0

def test_factory_aliases():
    assert "+" in OPERATIONS
    assert "*" in OPERATIONS
    assert "/" in OPERATIONS
    assert OPERATIONS["+"](1,2) == 3.0

def test_unknown_operation():
    with pytest.raises(ValueError):
        create_calculation("pow", 2, 3)

def test_history_add_and_all():
    h = History()
    assert len(h) == 0
    c1 = create_calculation("sub", 10, 1)
    h.add(c1)
    assert len(h) == 1
    assert h.all()[0].compute() == 9.0
    h.clear()
    assert len(h) == 0
