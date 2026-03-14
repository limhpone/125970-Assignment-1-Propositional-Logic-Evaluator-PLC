from components.lexica import PropLogicLexer
from components.ast.statement import Expression, Expression_bool, Expression_logic, Operations
from sly import Parser


class PropLogicParser(Parser):
    """
    Parser for propositional logic expressions.
    Grammar:
        statement : expr
        expr      : expr OR expr
                  | expr AND expr
                  | LPAREN expr RPAREN
                  | TRUE
                  | FALSE
    Precedence: AND (∧) binds tighter than OR (∨).
    Builds an AST and returns the root Expression node.
    """
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = PropLogicLexer.tokens
    precedence = (
        ('left', OR),
        ('left', AND),
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr OR expr')
    def expr(self, p) -> Expression:
        return Expression_logic(Operations.OR, p.expr0, p.expr1)

    @_('expr AND expr')
    def expr(self, p) -> Expression:
        return Expression_logic(Operations.AND, p.expr0, p.expr1)

    @_('LPAREN expr RPAREN')
    def expr(self, p) -> Expression:
        return p.expr

    @_('TRUE')
    def expr(self, p) -> Expression:
        return Expression_bool(True)

    @_('FALSE')
    def expr(self, p) -> Expression:
        return Expression_bool(False)


if __name__ == "__main__":
    lexer = PropLogicLexer()
    parser = PropLogicParser()

    # Test: t ∨ f ∧ f  → should be t (∧ binds tighter, so f∧f=f, then t∨f=t)
    text = "t ∨ f ∧ f"
    result = parser.parse(lexer.tokenize(text))
    if result:
        value = result.run()
        print(f"Expression: {text}")
        print(f"Truth Value: {'t' if value else 'f'}")
        print(f"Prefix: {result.prefix()}")