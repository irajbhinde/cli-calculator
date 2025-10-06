
"""Factory for creating calculation objects from tokens."""
from __future__ import annotations
from typing import Callable, Mapping
from .calculation import Calculation
from app.operation import add, sub, mul, div

OPERATIONS: Mapping[str, Callable[..., float]] = {
    "add": add,
    "+": add,
    "sub": sub,
    "-": sub,
    "mul": mul,
    "*": mul,
    "times": mul,
    "div": div,
    "/": div,
}

def create_calculation(op_name: str, *operands: float) -> Calculation:
    op = OPERATIONS.get(op_name.lower())
    if op is None:
        raise ValueError(f"Unknown operation: {op_name}")
    return Calculation(op_name, op, tuple(float(x) for x in operands))

__all__ = ["create_calculation", "OPERATIONS"]
