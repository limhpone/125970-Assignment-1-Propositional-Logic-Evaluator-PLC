# Propositional Logic Evaluator

Aye Khin Khin Hpone (Yolanda Lim)_st125970

Assignment 1 — Programming Language and Compiler course @ AIT (January 2026)

A propositional logic evaluator with two operators:
- **∧** (and) — higher precedence
- **∨** (or) — lower precedence

Given an input expression, the program outputs:
1. A **truth value** (`t` or `f`)
2. An equivalent expression in **prefix notation**

## Dependencies

- Python >= 3.10
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for managing the project
- `PySide6` for GUI
- `sly` for lexer/parser generation

## Getting Started

1. Clone the project to your local machine.
2. Run `uv sync` in the project root.

### Running

Press <kbd>F5</kbd> in VS Code to launch using the `[125970eval] Python Debugger` config.

Or use the terminal:

```sh
cd src/125970eval
uv run main.py
```

## Project Structure

```txt
src/125970eval/
  |- components/
      |- ast/
          |- statement.py
      |- lexica.py
      |- parsers.py
      |- ui.py
  |- main.py
```

### components/lexica.py

`PropLogicLexer` (extends `sly.Lexer`) — tokenises input into `TRUE`, `FALSE`, `AND`, `OR`, `LPAREN`, `RPAREN`. Accepts both Unicode (`∧` `∨`) and ASCII (`&` `|`) operators.

### components/parsers.py

`PropLogicParser` (extends `sly.Parser`) — builds an AST from the token stream. Operator precedence: AND binds tighter than OR (both left-associative).

### components/ast/statement.py

AST node classes:
- `Expression_bool` — leaf node holding a boolean value.
- `Expression_logic` — binary node holding an operation (AND/OR) and two children.

Each node implements `run()` (evaluate to `bool`) and `prefix()` (generate prefix notation string).

### components/ui.py

`Ui_MainWindow` — PySide6 GUI layout with buttons for `t`, `f`, `∧`, `∨`, `(`, `)`, Clear, and Evaluate, plus output labels for the truth value and prefix expression.

### main.py

Entry point — creates the GUI window and wires button clicks to the lexer → parser → AST evaluation pipeline.

## Examples

| Input       | Truth Value | Prefix Notation     |
|-------------|-------------|---------------------|
| `t`         | `t`         | `t`                 |
| `f`         | `f`         | `f`                 |
| `t∧f`       | `f`         | `(∧ t f)`           |
| `t∨f`       | `t`         | `(∨ t f)`           |
| `t∨f∧f`     | `t`         | `(∨ t (∧ f f))`     |
| `(t∨f)∧f`   | `f`         | `(∧ (∨ t f) f)`     |
