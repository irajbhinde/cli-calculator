
"""Command-line REPL for the calculator application."""
from __future__ import annotations
from typing import Iterable
from app.calculation.calculation import History
from app.calculation.factory import create_calculation

WELCOME = """CLI Calculator
Type 'help' for instructions or 'exit' to quit.
"""

HELP_TEXT = """Usage:
  <operation> <n1> <n2> [n3 ...]
Operations:
  add (+), sub (-), mul (* or times), div (/)
Special:
  help      Show this message
  history   Show previous calculations this session
  exit      Quit the program
Examples:
  add 1 2 3
  * 2 8
  div 10 2
"""

def parse_line(line: str) -> tuple[str, list[float]]:
    parts = line.strip().split()
    if not parts:
        raise ValueError("Empty input")
    op, *rest = parts
    try:
        nums = [float(x) for x in rest]
    except ValueError as e:
        raise ValueError("All operands must be numbers") from e
    return op, nums

def format_calc(op: str, nums: Iterable[float], result: float) -> str:
    nums_str = ", ".join(str(int(n)) if n.is_integer() else str(n) for n in nums)
    return f"{op}({nums_str}) = {result}"

def repl(stdin=input, stdout=print) -> None:
    from app.calculation.factory import OPERATIONS  # local import keeps CLI lightweight
    history = History()
    stdout(WELCOME)
    while True:
        stdout("")  # spacing
        line = stdin("calc> ")
        if line is None:  # pragma: no cover - interactive guards
            break
        line = line.strip()
        if not line:
            continue
        cmd = line.lower()
        if cmd in ("exit", "quit"):
            stdout("Bye!")
            break
        if cmd == "help":
            stdout(HELP_TEXT)
            continue
        if cmd == "history":
            if len(history) == 0:
                stdout("(no calculations yet)")
            else:
                for item in history.all():
                    stdout(format_calc(item.operation_name, item.operands, item.compute()))
            continue

        # Otherwise treat as calculation
        try:
            op, nums = parse_line(line)
        except ValueError as e:
            stdout(f"Error: {e}")
            continue
        try:
            # Check operation existence early (LBYL) to craft a nice error
            from app.calculation.factory import OPERATIONS
            if op.lower() not in OPERATIONS:
                raise ValueError(f"Unknown operation: {op}")
            calc = create_calculation(op, *nums)
            result = calc.compute()
            history.add(calc)
            stdout(format_calc(op, nums, result))
        except Exception as e:  # broad by design at REPL boundary
            stdout(f"Error: {e}")

def main() -> None:
    repl()

if __name__ == "__main__":  # pragma: no cover
    main()
