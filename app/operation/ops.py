
"""Arithmetic operation functions with type-safety and errors."""
from typing import Iterable

Number = float  # alias for readability

def _coerce_numbers(values: Iterable[object]) -> list[Number]:
    # LBYL: validate inputs before computing
    coerced: list[Number] = []
    for v in values:
        try:
            coerced.append(float(v))
        except (TypeError, ValueError) as e:
            raise ValueError(f"Not a number: {v!r}") from e
    return coerced

def add(*args: object) -> Number:
    """Return the sum of all arguments."""
    nums = _coerce_numbers(args)
    return sum(nums)

def sub(*args: object) -> Number:
    """Return a - b - c ... for the given arguments."""
    nums = _coerce_numbers(args)
    if not nums:
        raise ValueError("sub requires at least one number")
    head, *rest = nums
    return head - sum(rest)

def mul(*args: object) -> Number:
    """Return the product of all arguments."""
    nums = _coerce_numbers(args)
    if not nums:
        raise ValueError("mul requires at least one number")
    result: Number = 1.0
    for n in nums:
        result *= n
    return result

def div(*args: object) -> Number:
    """Return a / b / c ... for the given arguments.
    Uses EAFP: tries division and catches ZeroDivisionError if it occurs.
    """
    nums = _coerce_numbers(args)
    if not nums:
        raise ValueError("div requires at least one number")
    result: Number = nums[0]
    for n in nums[1:]:
        try:
            result /= n  # EAFP: perform and handle errors
        except ZeroDivisionError as e:
            raise ZeroDivisionError("Division by zero") from e
    return result
