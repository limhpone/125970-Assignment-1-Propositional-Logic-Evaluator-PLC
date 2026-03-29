# Propositional Logic Evaluator — Assignment 1 Report

> **Course:** Programming Language and Compiler (PLC)  
> **Institution:** Asian Institute of Technology (AIT)  
> **Trimester:** January 2026  
> **Author:** Aye Khin Khin Hpone (Yolanda Lim) — st125970  
> **Date:** March 15, 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Problem Statement](#2-problem-statement)
3. [Theoretical Background](#3-theoretical-background)
   - 3.1 [Propositional Logic](#31-propositional-logic)
   - 3.2 [Compiler Front-End Pipeline](#32-compiler-front-end-pipeline)
   - 3.3 [Notation Systems](#33-notation-systems)
4. [Language Design](#4-language-design)
   - 4.1 [Alphabet and Token Specification](#41-alphabet-and-token-specification)
   - 4.2 [Context-Free Grammar](#42-context-free-grammar)
   - 4.3 [Operator Precedence and Associativity](#43-operator-precedence-and-associativity)
5. [System Architecture](#5-system-architecture)
   - 5.1 [High-Level Pipeline](#51-high-level-pipeline)
   - 5.2 [Project Structure](#52-project-structure)
6. [Implementation Details](#6-implementation-details)
   - 6.1 [Lexical Analyser](#61-lexical-analyser)
   - 6.2 [Parser (LALR(1))](#62-parser-lalr1)
   - 6.3 [Abstract Syntax Tree (AST)](#63-abstract-syntax-tree-ast)
   - 6.4 [Evaluation — Truth Value Computation](#64-evaluation--truth-value-computation)
   - 6.5 [Translation — Prefix Notation Generation](#65-translation--prefix-notation-generation)
   - 6.6 [Graphical User Interface](#66-graphical-user-interface)
7. [Test Cases and Verification](#7-test-cases-and-verification)
8. [Tools and Technologies](#8-tools-and-technologies)
9. [Conclusion](#9-conclusion)
10. [References](#10-references)

---

## 1. Introduction

This report presents the design and implementation of a **Propositional Logic Evaluator**, developed as Assignment 1 for the Programming Language and Compiler (PLC) course at the Asian Institute of Technology. The evaluator accepts propositional logic expressions composed of truth values and logical connectives, then produces two outputs: the **evaluated truth value** and an equivalent expression in **prefix (Polish) notation**.

The project demonstrates core compiler front-end concepts — lexical analysis, syntactic parsing, abstract syntax tree construction, and tree-based evaluation/translation — applied to a simple yet formally defined language of propositional logic.

---

## 2. Problem Statement

**Objective:** Build an evaluator for a propositional logic language with two operators:

| Operator | Symbol | Meaning | Precedence |
|:--------:|:------:|:-------:|:----------:|
| AND | ∧ | Logical conjunction | **Higher** (binds tighter) |
| OR  | ∨ | Logical disjunction | **Lower** |

**Inputs:** A propositional logic expression using truth values (`t`, `f`), operators (`∧`, `∨`), and parentheses.

**Required Outputs:**
1. A **truth value** — the result of evaluating the expression (`t` or `f`)
2. An equivalent expression in **prefix notation**

**Example:**

```
Input:    t ∨ f ∧ f
Output:   Truth Value = t
          Prefix      = (∨ t (∧ f f))
```

---

## 3. Theoretical Background

### 3.1 Propositional Logic

Propositional logic is a branch of mathematical logic that deals with propositions — statements that are either **true** or **false**. Propositions are combined using **logical connectives** to form compound expressions:

- **Conjunction (∧):** $p \land q$ is true only when **both** $p$ and $q$ are true.
- **Disjunction (∨):** $p \lor q$ is true when **at least one** of $p$ or $q$ is true.

**Truth tables** for the two operators in this evaluator:

| $p$ | $q$ | $p \land q$ | $p \lor q$ |
|:---:|:---:|:----------:|:----------:|
| t | t | t | t |
| t | f | f | t |
| f | t | f | t |
| f | f | f | f |

### 3.2 Compiler Front-End Pipeline

A typical compiler front-end processes source code through a series of phases:

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Source      │    │   Lexical    │    │   Syntax     │    │   Semantic   │
│   Code        │───▶│   Analysis   │───▶│   Analysis   │───▶│   Analysis   │
│   (string)    │    │   (Lexer)    │    │   (Parser)   │    │   (AST)      │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                      tokens               parse tree          evaluated result
```

1. **Lexical Analysis (Lexer/Scanner):** Reads the input character stream and groups characters into meaningful units called **tokens** (e.g., keywords, operators, literals).

2. **Syntactic Analysis (Parser):** Takes the token stream and validates it against a **formal grammar**, building a structured representation — typically a **parse tree** or **abstract syntax tree (AST)**.

3. **Semantic Analysis / Evaluation:** Traverses the AST to compute results (evaluation) or produce alternative representations (translation).

This project implements all three phases.

### 3.3 Notation Systems

Mathematical expressions can be written in three different notations:

| Notation | Name | Example | Description |
|:--------:|:----:|:-------:|:------------|
| **Infix** | Standard | `t ∧ f` | Operator **between** operands |
| **Prefix** | Polish | `(∧ t f)` | Operator **before** operands |
| **Postfix** | Reverse Polish | `t f ∧` | Operator **after** operands |

**Prefix notation** (also known as **Polish notation**, invented by Jan Łukasiewicz) places the operator before its operands. When fully parenthesised, each sub-expression is enclosed in parentheses for unambiguous reading:

$$\text{Infix: } t \lor (f \land f) \quad \Longrightarrow \quad \text{Prefix: } (\lor\ t\ (\land\ f\ f))$$

The key advantage of prefix notation is that it **eliminates the need for precedence rules** — the structure is fully explicit.

---

## 4. Language Design

### 4.1 Alphabet and Token Specification

The input language recognises the following symbols, each mapped to a token type:

| Token Name | Regular Expression | Matches | Description |
|:----------:|:-----------------:|:-------:|:------------|
| `TRUE` | `t` | `t` | Boolean true literal |
| `FALSE` | `f` | `f` | Boolean false literal |
| `AND` | `[∧&]` | `∧` or `&` | Conjunction operator |
| `OR` | `[∨\|]` | `∨` or `\|` | Disjunction operator |
| `LPAREN` | `\(` | `(` | Left parenthesis |
| `RPAREN` | `\)` | `)` | Right parenthesis |

**Design decision:** Both Unicode symbols (`∧`, `∨`) and ASCII alternatives (`&`, `|`) are accepted. This provides flexibility for environments where Unicode input may be difficult, while the GUI buttons produce the standard Unicode symbols.

Whitespace (spaces and tabs) is **ignored** between tokens. Illegal characters trigger an error message.

### 4.2 Context-Free Grammar

The evaluator's syntax is defined by the following **context-free grammar (CFG)** in BNF-like notation:

$$
G = (V_N,\ V_T,\ P,\ S)
$$

Where:
- $V_N = \{\ \text{statement},\ \text{expr}\ \}$ — non-terminal symbols
- $V_T = \{\ \texttt{TRUE},\ \texttt{FALSE},\ \texttt{AND},\ \texttt{OR},\ \texttt{LPAREN},\ \texttt{RPAREN}\ \}$ — terminal symbols
- $S = \text{statement}$ — start symbol
- $P$ — production rules:

```
Production Rules:
─────────────────────────────────────────────────
(1)  statement  →  expr
(2)  expr       →  expr  OR  expr
(3)  expr       →  expr  AND  expr
(4)  expr       →  LPAREN  expr  RPAREN
(5)  expr       →  TRUE
(6)  expr       →  FALSE
─────────────────────────────────────────────────
```

**Observations:**
- The grammar is **ambiguous** because rules (2) and (3) introduce two possible parse trees for expressions like `t ∨ f ∧ f`. This ambiguity is resolved through **precedence and associativity declarations** (Section 4.3).
- Rule (1) wraps the top-level expression, providing a single entry point.
- Rule (4) allows explicit grouping with parentheses to override default precedence.

### 4.3 Operator Precedence and Associativity

To disambiguate the grammar, operator precedence and associativity are declared:

| Precedence Level | Operator | Symbol | Associativity |
|:----------------:|:--------:|:------:|:-------------:|
| 1 (lower) | OR  | ∨ | Left |
| 2 (higher) | AND | ∧ | Left |

**Consequence:** In the expression `t ∨ f ∧ f`, the AND operator binds tighter than OR, producing the parse:

$$t \lor (f \land f) \quad \text{not} \quad (t \lor f) \land f$$

**Left associativity** means that for chains of the same operator, grouping proceeds from left to right:

$$t \lor f \lor f \quad = \quad (t \lor f) \lor f$$

These declarations are passed directly to the LALR(1) parser generator, which uses them to resolve shift/reduce conflicts in the parse table.

---

## 5. System Architecture

### 5.1 High-Level Pipeline

The system follows a classic compiler front-end pipeline with two output phases:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   Input      │     │   Lexer     │     │   Parser    │     │    AST          │
│   String     │────▶│  (Tokenise) │────▶│  (LALR(1))  │────▶│  Construction   │
│              │     │             │     │             │     │                 │
└─────────────┘     └─────────────┘     └─────────────┘     └────────┬────────┘
                                                                     │
                                                          ┌──────────┴──────────┐
                                                          │                     │
                                                    ┌─────▼─────┐        ┌──────▼──────┐
                                                    │  run()     │        │  prefix()   │
                                                    │ Evaluate   │        │ Translate   │
                                                    │ → t or f   │        │ → prefix    │
                                                    └───────────┘        └─────────────┘
```

**Data flow summary:**

| Phase | Input | Output | Component |
|:-----:|:-----:|:------:|:---------:|
| 1. Lexical Analysis | Character string | Token stream | `PropLogicLexer` |
| 2. Syntactic Analysis | Token stream | AST (tree) | `PropLogicParser` |
| 3a. Evaluation | AST | Boolean value (`t`/`f`) | `Expression.run()` |
| 3b. Translation | AST | Prefix string | `Expression.prefix()` |

### 5.2 Project Structure

```
src/125970eval/
│
├── main.py                          # Entry point — GUI + pipeline orchestration
│
└── components/
    ├── __init__.py
    ├── lexica.py                    # Lexical analyser (tokeniser)
    ├── parsers.py                   # LALR(1) parser (builds AST)
    ├── ui.py                        # PySide6 GUI layout definition
    │
    └── ast/
        ├── __init__.py
        └── statement.py             # AST node class hierarchy
```

---

## 6. Implementation Details

### 6.1 Lexical Analyser

**File:** `components/lexica.py`  
**Class:** `PropLogicLexer` (extends `sly.Lexer`)

The lexer converts an input string into a stream of tokens using **regular expression** pattern matching. Each token type is defined as a class attribute with a corresponding regex pattern.

**Token matching implementation:**

```python
tokens = { TRUE, FALSE, AND, OR, LPAREN, RPAREN }

AND    = r'[∧&]'      # Unicode ∧ or ASCII &
OR     = r'[∨|]'      # Unicode ∨ or ASCII |
LPAREN = r'\('
RPAREN = r'\)'
TRUE   = r't'
FALSE  = r'f'

ignore = ' \t'         # Skip whitespace
```

**Tokenisation example for `t ∨ f ∧ f`:**

| Position | Character | Token Type | Token Value |
|:--------:|:---------:|:----------:|:-----------:|
| 0 | `t` | `TRUE` | `t` |
| 2 | `∨` | `OR` | `∨` |
| 4 | `f` | `FALSE` | `f` |
| 6 | `∧` | `AND` | `∧` |
| 8 | `f` | `FALSE` | `f` |

Whitespace at positions 1, 3, 5, 7 is silently consumed by the `ignore` directive.

**Error handling:** The `error()` method raises a `ValueError` with a descriptive message identifying the illegal character and its position. This exception propagates up to the GUI, which displays the error to the user (e.g., `Error: Illegal character 'x' at position 5`).

### 6.2 Parser (LALR(1))

**File:** `components/parsers.py`  
**Class:** `PropLogicParser` (extends `sly.Parser`)  
**Algorithm:** LALR(1) — Look-Ahead LR with 1 token of lookahead

#### 6.2.1 What is LALR(1)?

**LALR(1)** (Look-Ahead Left-to-right Rightmost-derivation) is a **bottom-up** parsing algorithm that:

- Reads input **left to right** (L)
- Produces a **rightmost derivation** in reverse (R)
- Uses **1 token** of lookahead to make parsing decisions

It is the most widely used parser algorithm in practice, balancing the power of LR(1) parsing with the compactness of SLR(1) parse tables. The SLY library automatically generates the LALR(1) parse table from the grammar rules and precedence declarations.

#### 6.2.2 Bottom-Up Parsing Process

The parser uses a **shift-reduce** mechanism:

- **Shift:** Push the next input token onto the parse stack.
- **Reduce:** When the top of the stack matches the right side of a production rule, replace it with the left side (non-terminal) and execute the associated **semantic action** (AST node construction).

**Parsing trace for `t ∨ f ∧ f`:**

| Step | Stack | Input | Action | Semantic Action |
|:----:|:------|:------|:------:|:----------------|
| 1 | — | `t ∨ f ∧ f` | Shift `t` | — |
| 2 | `TRUE` | `∨ f ∧ f` | Reduce (5) | Create `Expression_bool(True)` |
| 3 | `expr` | `∨ f ∧ f` | Shift `∨` | — |
| 4 | `expr ∨` | `f ∧ f` | Shift `f` | — |
| 5 | `expr ∨ FALSE` | `∧ f` | Reduce (6) | Create `Expression_bool(False)` |
| 6 | `expr ∨ expr` | `∧ f` | Shift `∧` ¹ | — |
| 7 | `expr ∨ expr ∧` | `f` | Shift `f` | — |
| 8 | `expr ∨ expr ∧ FALSE` | — | Reduce (6) | Create `Expression_bool(False)` |
| 9 | `expr ∨ expr ∧ expr` | — | Reduce (3) | Create `Expression_logic(AND, ...)` |
| 10 | `expr ∨ expr` | — | Reduce (2) | Create `Expression_logic(OR, ...)` |
| 11 | `statement` | — | Accept | Return root AST node |

> ¹ At step 6, there is a **shift/reduce conflict**: the parser could either reduce `expr ∨ expr` (rule 2) or shift `∧`. Because AND has **higher precedence** than OR, the parser chooses to **shift**, correctly binding `∧` tighter.

#### 6.2.3 Precedence Conflict Resolution

The SLY parser resolves shift/reduce conflicts using the declared precedence:

```python
precedence = (
    ('left', OR),     # Level 1 — lower priority
    ('left', AND),    # Level 2 — higher priority (listed last = highest)
)
```

**Rule:** When the parser encounters a conflict between shifting a token and reducing by a rule, it compares the precedence of the lookahead token with the precedence of the rule. If the token has higher precedence, it shifts; otherwise, it reduces.

#### 6.2.4 Grammar Rules with Semantic Actions

Each grammar rule constructs an AST node:

```python
@_('expr OR expr')
def expr(self, p) -> Expression:
    return Expression_logic(Operations.OR, p.expr0, p.expr1)

@_('expr AND expr')
def expr(self, p) -> Expression:
    return Expression_logic(Operations.AND, p.expr0, p.expr1)

@_('TRUE')
def expr(self, p) -> Expression:
    return Expression_bool(True)

@_('FALSE')
def expr(self, p) -> Expression:
    return Expression_bool(False)
```

The semantic actions are **syntax-directed**: each grammar rule directly constructs the corresponding AST node, building the tree bottom-up as reductions occur.

### 6.3 Abstract Syntax Tree (AST)

**File:** `components/ast/statement.py`

The AST represents the hierarchical structure of propositional logic expressions. It is implemented using three classes in an **inheritance hierarchy**:

```
            Expression (ABC)
           ┌──────┴──────┐
  Expression_bool    Expression_logic
    (leaf node)       (binary node)
```

#### 6.3.1 Class Hierarchy

| Class | Role | Fields | Methods |
|:------|:-----|:-------|:--------|
| `Expression` | Abstract base class | `value` | `run()`, `prefix()` (abstract) |
| `Expression_bool` | Leaf: truth literal | `value: bool` | `run()` → bool, `prefix()` → `"t"` or `"f"` |
| `Expression_logic` | Binary: logical op | `operation`, `left`, `right` | `run()` → recursive eval, `prefix()` → prefix string |

The `Operations` enum defines the two logical operations:

```python
class Operations(Enum):
    AND = 0
    OR  = 1
```

#### 6.3.2 AST Construction Example

For the expression `t ∨ f ∧ f`, the parser builds the following AST:

```
          Expression_logic
          operation: OR
          ┌──────┴──────┐
          │              │
  Expression_bool   Expression_logic
  value: True       operation: AND
                    ┌──────┴──────┐
                    │              │
            Expression_bool   Expression_bool
            value: False      value: False
```

This tree correctly reflects that `∧` binds tighter than `∨`, grouping `f ∧ f` as a subtree under the `∨` node.

### 6.4 Evaluation — Truth Value Computation

**Method:** `Expression.run()` — recursive, bottom-up tree traversal

The `run()` method computes the truth value by recursively evaluating child nodes:

**For leaf nodes (`Expression_bool`):**

$$\text{run}() = \text{value} \in \{True, False\}$$

**For binary nodes (`Expression_logic`):**

$$\text{run}() = \begin{cases} \text{left.run()} \wedge \text{right.run()} & \text{if operation} = \text{AND} \\[4pt] \text{left.run()} \vee \text{right.run()} & \text{if operation} = \text{OR} \end{cases}$$

**Evaluation trace for `t ∨ f ∧ f`:**

```
run(OR)
├── run(Bool: t) = True
└── run(AND)
    ├── run(Bool: f) = False
    └── run(Bool: f) = False
    = False ∧ False = False
= True ∨ False = True → 't'
```

### 6.5 Translation — Prefix Notation Generation

**Method:** `Expression.prefix()` — recursive, pre-order tree traversal

The `prefix()` method converts the AST into a fully parenthesised prefix notation string:

**For leaf nodes:**

$$\text{prefix}() = \begin{cases} \texttt{"t"} & \text{if value is True} \\ \texttt{"f"} & \text{if value is False} \end{cases}$$

**For binary nodes:**

$$\text{prefix}() = \texttt{"("} + op + \texttt{" "} + \text{left.prefix()} + \texttt{" "} + \text{right.prefix()} + \texttt{")"}$$

where $op \in \{∧, ∨\}$ corresponds to the node's operation.

**Translation trace for `t ∨ f ∧ f`:**

```
prefix(OR)
├── prefix(Bool: t) = "t"
└── prefix(AND)
    ├── prefix(Bool: f) = "f"
    └── prefix(Bool: f) = "f"
    = "(∧ f f)"
= "(∨ t (∧ f f))"
```

**Key property:** The prefix output is **fully parenthesised**, making operator grouping explicit without relying on precedence rules. This ensures the prefix string is an unambiguous representation of the evaluated AST.

### 6.6 Graphical User Interface

**Files:** `components/ui.py` (layout) + `main.py` (logic)  
**Framework:** PySide6 (Qt6 for Python)

The GUI provides an interactive calculator-style interface:

```
┌──────────────────────────────────────────────┐
│  Propositional Logic Evaluator               │
├──────────────────────────────────────────────┤
│  Input:  [ t ∨ f ∧ f                      ] │
│                                              │
│  [ t ] [ f ] [ ∧ ] [ ∨ ] [ ( ] [ ) ]       │
│  [    Clear    ] [       = Evaluate       ]  │
│                                              │
│  Truth Value:    t                           │
│  Prefix Notation: (∨ t (∧ f f))             │
└──────────────────────────────────────────────┘
```

**UI components:**

| Component | Type | Purpose |
|:----------|:-----|:--------|
| Input field | `QLineEdit` | Displays and accepts the input expression |
| Symbol buttons (×6) | `QPushButton` | Insert `t`, `f`, `∧`, `∨`, `(`, `)` into input |
| Clear button | `QPushButton` | Resets all fields |
| Evaluate button | `QPushButton` | Triggers the lexer → parser → AST pipeline |
| Truth Value output | `QLabel` | Displays evaluated result |
| Prefix Notation output | `QLabel` | Displays prefix expression |

**Pipeline wiring in `main.py`:**

When the user clicks **Evaluate**, the `evaluate()` method:
1. Creates fresh `PropLogicLexer` and `PropLogicParser` instances.
2. Tokenises the input text.
3. Parses the token stream to build the AST.
4. Calls `result.run()` for the truth value.
5. Calls `result.prefix()` for the prefix notation.
6. Displays both results in the output labels.
7. Catches and displays errors for invalid expressions.

---

## 7. Test Cases and Verification

All six required test cases were verified to produce the correct output:

| # | Input | Expected Truth Value | Expected Prefix | Actual Truth Value | Actual Prefix | Status |
|:-:|:------|:--------------------:|:----------------|:------------------:|:--------------|:------:|
| 1 | `t` | `t` | `t` | `t` | `t` | ✅ |
| 2 | `f` | `f` | `f` | `f` | `f` | ✅ |
| 3 | `t ∧ f` | `f` | `(∧ t f)` | `f` | `(∧ t f)` | ✅ |
| 4 | `t ∨ f` | `t` | `(∨ t f)` | `t` | `(∨ t f)` | ✅ |
| 5 | `t ∨ f ∧ f` | `t` | `(∨ t (∧ f f))` | `t` | `(∨ t (∧ f f))` | ✅ |
| 6 | `(t ∨ f) ∧ f` | `f` | `(∧ (∨ t f) f)` | `f` | `(∧ (∨ t f) f)` | ✅ |

An automated test suite (`tests/test_evaluator.py`) executed with **pytest** contains **12 tests** in three groups: 6 core test cases (above), 3 ASCII-operator equivalence tests (`&` and `|`), and 3 error-handling tests (illegal character raises `ValueError`, incomplete expression returns `None`, empty input returns `None`). All 12 tests pass.

**Explanation of key test cases:**

- **Test 5** (`t ∨ f ∧ f`): Validates **operator precedence**. AND binds tighter than OR, so `f ∧ f = f` is evaluated first, then `t ∨ f = t`. The prefix correctly nests the AND as a subtree: `(∨ t (∧ f f))`.

- **Test 6** (`(t ∨ f) ∧ f`): Validates **parenthesised grouping** overriding default precedence. The parentheses force OR to be evaluated first: `t ∨ f = t`, then `t ∧ f = f`. The prefix reflects this: `(∧ (∨ t f) f)`.

---

## 8. Tools and Technologies

| Technology | Version | Purpose |
|:-----------|:-------:|:--------|
| **Python** | ≥ 3.10 | Core implementation language |
| **SLY** | latest (GitHub master) | Lexer and LALR(1) parser generator |
| **PySide6** | ≥ 6.10.2 | Qt6-based GUI framework |
| **uv** | latest | Python package and virtual environment manager |
| **VS Code** | latest | Development environment with integrated debugger |

### About SLY

[SLY (Sly Lex Yacc)](https://github.com/dabeaz/sly) is a Python library by David Beazley that provides:

- **Lexer generator** — defines tokens via regular expressions as class attributes.
- **Parser generator** — accepts grammar rules as decorated methods and generates an **LALR(1) parse table** automatically.
- **Conflict resolution** — uses declared `precedence` tuples to resolve shift/reduce conflicts.
- **Debug output** — writes `parser.out` containing the full LALR(1) state machine, parse table, and any grammar conflicts for inspection.

SLY was chosen for this project because it provides a clean, Pythonic API that closely maps to formal grammar notation, making the connection between theory and implementation transparent.

---

## 9. Conclusion

This project successfully implements a **propositional logic evaluator** that:

1. **Lexes** input expressions into tokens using regular expression-based pattern matching.
2. **Parses** token streams into an AST using an **LALR(1) bottom-up parser** with correctly declared operator precedence (AND > OR).
3. **Evaluates** the AST via recursive bottom-up traversal (`run()`) to produce a truth value.
4. **Translates** the AST via recursive pre-order traversal (`prefix()`) to produce fully parenthesised prefix notation.
5. Provides an interactive **GUI** for convenient expression input and result display.

The implementation demonstrates the direct application of **compiler front-end theory** — lexical analysis, formal grammars, LALR(1) parsing, syntax-directed translation, and AST-based evaluation — to a well-defined problem domain. All six test cases produce correct results, confirming that operator precedence, associativity, and parenthesised grouping are handled correctly.

---

## 10. References

1. Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.

2. Beazley, D. (2023). SLY (Sly Lex Yacc). GitHub. https://github.com/dabeaz/sly

3. SLY Documentation. https://sly.readthedocs.io/en/latest/sly.html

4. The Qt Company. (2025). Qt for Python (PySide6) Documentation. https://doc.qt.io/qtforpython-6/

5. Łukasiewicz, J. (1957). *Aristotle's Syllogistic from the Standpoint of Modern Formal Logic* (2nd ed.). Oxford University Press. *(Origin of Polish/prefix notation)*
