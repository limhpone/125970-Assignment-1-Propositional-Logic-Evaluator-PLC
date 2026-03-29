from sly import Lexer

class PropLogicLexer(Lexer):
    """
    Lexer for propositional logic expressions.
    Tokens: TRUE (t), FALSE (f), AND (∧ or &), OR (∨ or |), LPAREN, RPAREN
    ref: https://sly.readthedocs.io/en/latest/sly.html#sly-sly-lex-yacc
    """

    # All tokens must be listed here (capitalized)
    tokens = { TRUE, FALSE, AND, OR, LPAREN, RPAREN }

    # Ignore spaces and tabs
    ignore = ' \t'

    # Operator tokens — support both Unicode and ASCII alternatives
    AND    = r'[∧&]'
    OR     = r'[∨|]'
    LPAREN = r'\('
    RPAREN = r'\)'
    TRUE   = r't'
    FALSE  = r'f'

    # Extra action for newlines
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        bad = t.value[0]
        self.index += 1
        raise ValueError(f"Illegal character '{bad}' at position {self.index}")

if __name__ == '__main__':
    string_input: str = "t ∧ f ∨ t"
    lex = PropLogicLexer()
    for token in lex.tokenize(string_input):
        print(token)