
# CLI Calculator (Professional-Grade, Tested, CI-Enforced)

A modular, professional-grade command-line calculator in Python featuring a REPL, solid error handling (LBYL + EAFP), history, and full test coverage enforced by GitHub Actions.

## Features
- REPL with `help`, `history`, `exit`
- Operations: add/sub/mul/div (and aliases `+ - * / times`)
- Input validation & friendly errors
- Calculation objects, Factory pattern, and session History
- pytest test-suite with parameterized tests
- **100% coverage** enforced in CI

## Project Layout
```
app/
  calculator/
    __init__.py
    cli.py
  calculation/
    __init__.py
    calculation.py
    factory.py
  operation/
    __init__.py
    ops.py
tests/
  test_cli.py
  test_calculations.py
  test_operations.py
.github/workflows/python-app.yml
.coveragerc
README.md
requirements.txt
pyproject.toml
```

## Getting Started

### 1) Create & activate a virtual environment
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 2) Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Run tests with coverage
```bash
pytest --cov=app --cov-branch -q
coverage report --fail-under=100
```

### 4) Run the calculator
```bash
python -m app.calculator.cli
# or
python -c "from app.calculator import main; main()"
```

## Notes on Coverage Exceptions
- Lines that are inherently untestable (e.g., interactive guards) are marked with `# pragma: no cover`.
- We still achieve 100% overall coverage with the provided tests.

## GitHub Actions
A workflow is provided at `.github/workflows/python-app.yml` which:
- Checks out code
- Sets up Python
- Installs deps
- Runs tests with coverage
- Fails the build if coverage < 100%

## Contributing / Development
- Follow DRY and keep modules cohesive.
- Prefer pure functions and small classes.
- Add tests for every branch & edge-case.
