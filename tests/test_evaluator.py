"""
Automated test suite for the Propositional Logic Evaluator.
Covers the 6 core test cases (truth value + prefix notation)
and error-handling behaviour.
"""

import sys, os
import pytest

# Add src directory to path so imports resolve without installing the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', '125970eval'))

from components.lexica import PropLogicLexer
from components.parsers import PropLogicParser


# ── helpers ──────────────────────────────────────────────────────────

def evaluate(expr: str):
    """Parse *expr* and return (truth_value_str, prefix_str)."""
    lexer = PropLogicLexer()
    parser = PropLogicParser()
    result = parser.parse(lexer.tokenize(expr))
    assert result is not None, f"Parser returned None for '{expr}'"
    truth = 't' if result.run() else 'f'
    return truth, result.prefix()


# ── 6 core test cases (Table 5.1 in the report) ─────────────────────

class TestCoreCases:
    """Six representative test cases covering literals, operators,
    precedence, and parenthesised grouping."""

    def test_true_literal(self):
        val, pfx = evaluate("t")
        assert val == 't'
        assert pfx == 't'

    def test_false_literal(self):
        val, pfx = evaluate("f")
        assert val == 'f'
        assert pfx == 'f'

    def test_conjunction(self):
        val, pfx = evaluate("t ∧ f")
        assert val == 'f'
        assert pfx == '(∧ t f)'

    def test_disjunction(self):
        val, pfx = evaluate("t ∨ f")
        assert val == 't'
        assert pfx == '(∨ t f)'

    def test_precedence(self):
        """∧ binds tighter than ∨: t ∨ f ∧ f  ≡  t ∨ (f ∧ f) = t"""
        val, pfx = evaluate("t ∨ f ∧ f")
        assert val == 't'
        assert pfx == '(∨ t (∧ f f))'

    def test_parenthesised_grouping(self):
        """Parentheses override default precedence."""
        val, pfx = evaluate("(t ∨ f) ∧ f")
        assert val == 'f'
        assert pfx == '(∧ (∨ t f) f)'


# ── ASCII alternative operators ──────────────────────────────────────

class TestASCIIOperators:
    """Ensure the lexer accepts & and | as alternatives to ∧ and ∨."""

    def test_ascii_and(self):
        val, pfx = evaluate("t & f")
        assert val == 'f'
        assert pfx == '(∧ t f)'

    def test_ascii_or(self):
        val, pfx = evaluate("t | f")
        assert val == 't'
        assert pfx == '(∨ t f)'

    def test_ascii_precedence(self):
        val, pfx = evaluate("t | f & f")
        assert val == 't'
        assert pfx == '(∨ t (∧ f f))'


# ── Error handling ───────────────────────────────────────────────────

class TestErrorHandling:

    def test_illegal_character(self):
        """Lexer should raise ValueError on unrecognised characters."""
        lexer = PropLogicLexer()
        parser = PropLogicParser()
        with pytest.raises(ValueError, match="Illegal character"):
            parser.parse(lexer.tokenize("t ∧ x"))

    def test_syntax_error_returns_none(self):
        """Incomplete expression should make the parser return None."""
        lexer = PropLogicLexer()
        parser = PropLogicParser()
        result = parser.parse(lexer.tokenize("t ∧"))
        assert result is None

    def test_empty_input_returns_none(self):
        lexer = PropLogicLexer()
        parser = PropLogicParser()
        result = parser.parse(lexer.tokenize(""))
        assert result is None
