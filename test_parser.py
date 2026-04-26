import unittest

from parser import Statement, StatementType

class TestParser(unittest.TestCase):
    
    def test_parser_eof(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer(""))
        want = Statement(StatementType.RETURN)
        got = parser.get_next_statement()
        self.assertEqual(got, want)

    def test_parser_onenumber(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("1;"))
        want = Statement(StatementType.INT_ATOM, 1)
        got = parser.get_next_statement()
        self.assertEqual(got, want)

if __name__ == '__main__':
    unittest.main()