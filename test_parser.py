import unittest

from lexer import Token, TokenType
from parser import Node, NodeType, BinaryOp

class TestParser(unittest.TestCase):

    def test_parser_empty(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer(""))
        got = parser.get_next_node()
        self.assertEqual(got, None)

    def test_parser_onenumber(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("1;"))
        want = Node(NodeType.INT_ATOM, 1)
        got = parser.get_next_node()
        self.assertEqual(got, want)

    def test_parser_simpleadd(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("5 +7;"))
        want = Node(
            NodeType.EXPR_BINARY,
            [BinaryOp.PLUS, Node(NodeType.INT_ATOM, 5), Node(NodeType.INT_ATOM, 7)],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
