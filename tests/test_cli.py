import pytest
from app.calculator.cli import repl, parse_line, format_calc, HELP_TEXT

def run_repl_script(lines):
    # Helper to run the REPL with scripted input
    inputs = iter(lines)
    outputs = []
    def fake_input(prompt=""):
        try:
            return next(inputs)
        except StopIteration:
            return "exit"
    def fake_print(*args, **kwargs):
        outputs.append(" ".join(str(a) for a in args))
    repl(stdin=fake_input, stdout=fake_print)
    return outputs

def test_parse_line_and_format_calc():
    op, nums = parse_line("add 1 2 3")
    assert op == "add" and nums == [1.0, 2.0, 3.0]
    text = format_calc("add", [1.0, 2.0], 3.0)
    assert "add(1, 2) = 3.0" in text

def test_parse_line_empty_raises():
    # Covers the "Empty input" branch in parse_line
    with pytest.raises(ValueError):
        parse_line("   ")

def test_repl_help_history_and_exit():
    out = run_repl_script([
        "help",
        "add 1 2",
        "history",
        "exit",
    ])
    # Ensure welcome printed and help shown
    assert any("CLI Calculator" in line for line in out)
    assert any(HELP_TEXT.splitlines()[0] in line for line in out)
    # Calculation echoed and shown in history
    assert any("add(1, 2) = 3.0" in line for line in out)
    # Exit message
    assert any("Bye!" in line for line in out)

def test_repl_error_paths():
    out = run_repl_script([
        "",                 # empty = ignored
        "bogus 1 2",       # unknown op
        "add a b",         # invalid numbers
        "div 1 0",         # ZeroDivisionError
        "history",
        "exit",
    ])
    assert any("Unknown operation" in line for line in out)
    assert any("All operands must be numbers" in line for line in out)
    assert any("Division by zero" in line for line in out)
    # history should be empty (no successful calc before)
    assert any("(no calculations yet)" in line for line in out)

def test_repl_quit_alias():
    # Cover 'quit' alias path
    out = _run_script(["quit"])
    assert any("Bye!" in line for line in out)

def test_repl_keyboardinterrupt_exit():
    # Cover Ctrl+C branch
    def fake_input(_):
        raise KeyboardInterrupt
    outs = []
    def fake_print(*args, **kwargs):
        outs.append(" ".join(str(a) for a in args))
    repl(stdin=fake_input, stdout=fake_print)
    assert any("(CTRL+C) Bye!" in line for line in outs)

def test_repl_eof_exit():
    # Cover EOF branch (Ctrl+D / Ctrl+Z+Enter)
    def fake_input(_):
        raise EOFError
    outs = []
    def fake_print(*args, **kwargs):
        outs.append(" ".join(str(a) for a in args))
    repl(stdin=fake_input, stdout=fake_print)
    assert any("(EOF) Bye!" in line for line in outs)

def test_cli_symbol_and_word_aliases():
    # Covers symbol '*' and word 'times'
    out = _run_script([
        "* 2 3",
        "times 2 3",
        "history",
        "exit",
    ])
    assert any("*(2, 3) = 6.0" in line or "mul(2, 3) = 6.0" in line for line in out)  # format_calc prints op name used
    assert any("times(2, 3) = 6.0" in line or "mul(2, 3) = 6.0" in line for line in out)

def test_main_executes_repl_and_exits(monkeypatch):
    # Patch repl so main() can call it without real stdin/stdout
    called = {"ok": False}

    def fake_repl(stdin=input, stdout=print):
        called["ok"] = True  # mark that main() invoked repl()

    monkeypatch.setattr("app.calculator.cli.repl", fake_repl)

    from app.calculator.cli import main
    main()

    assert called["ok"] is True



# helper reused by earlier tests to drive the REPL
def _run_script(lines):
    inputs = iter(lines)
    outputs = []
    def fake_input(prompt=""):
        try:
            return next(inputs)
        except StopIteration:
            return "exit"
    def fake_print(*args, **kwargs):
        outputs.append(" ".join(str(a) for a in args))
    repl(stdin=fake_input, stdout=fake_print)
    return outputs
