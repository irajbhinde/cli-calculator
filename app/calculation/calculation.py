
"""Calculation objects and session history management."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True, slots=True)
class Calculation:
    """Represents a single calculation with an operation and operands."""
    operation_name: str
    operation: Callable[..., float]
    operands: tuple[float, ...]

    def compute(self) -> float:
        return self.operation(*self.operands)

class History:
    """Session-scoped calculation history."""
    def __init__(self) -> None:
        self._items: list[Calculation] = []

    def add(self, calc: Calculation) -> None:
        self._items.append(calc)

    def all(self) -> list[Calculation]:
        return list(self._items)

    def __len__(self) -> int:  # tiny convenience
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

__all__ = ["Calculation", "History"]
