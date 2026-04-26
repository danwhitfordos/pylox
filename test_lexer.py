import unittest

from lexer import TokenType, Token


class TestLexer(unittest.TestCase):

    def test_lexer_eof(self):
        from lexer import Lexer

        lexer = Lexer("")
        got = lexer.get_next_token()
        self.assertEqual(got.type, TokenType.EOF)

    def test_lexer_operands(self):
        from lexer import Lexer

        lexer = Lexer("+ - * /")
        want = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.MUL,
            TokenType.DIV,
            TokenType.EOF,
        ]
        for w in want:
            got = lexer.get_next_token()
            self.assertEqual(got.type, w)

    def test_lexer_expression(self):
        from lexer import Lexer

        lexer = Lexer("(1 + 2) * 3;")
        want = [
            Token(TokenType.LB),
            Token(TokenType.INTEGER, 1),
            Token(TokenType.PLUS),
            Token(TokenType.INTEGER, 2),
            Token(TokenType.RB),
            Token(TokenType.MUL),
            Token(TokenType.INTEGER, 3),
            Token(TokenType.SEMICOLON),
            Token(TokenType.EOF),
        ]

        for w in want:
            got = lexer.get_next_token()
            self.assertEqual(got, w)


if __name__ == "__main__":
    unittest.main()
