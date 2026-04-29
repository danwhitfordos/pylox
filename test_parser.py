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

    def test_parser_multiadd(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("1+2+3;"))
        want = Node(
            NodeType.EXPR_BINARY,
            [
                BinaryOp.PLUS,
                Node(
                    NodeType.EXPR_BINARY,
                    [
                        BinaryOp.PLUS,
                        Node(NodeType.INT_ATOM, 1),
                        Node(NodeType.INT_ATOM, 2),
                    ],
                ),
                Node(NodeType.INT_ATOM, 3),
            ],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)

    def test_parser_two_expressions(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("1+2; 2 + 3 ;"))
        want_a = Node(
            NodeType.EXPR_BINARY,
            [
                BinaryOp.PLUS,
                Node(NodeType.INT_ATOM, 1),
                Node(NodeType.INT_ATOM, 2),
            ],
        )
        want_b = Node(
            NodeType.EXPR_BINARY,
            [
                BinaryOp.PLUS,
                Node(NodeType.INT_ATOM, 2),
                Node(NodeType.INT_ATOM, 3),
            ],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want_a)
        got = parser.get_next_node()
        self.assertEqual(got, want_b)

    def test_parser_minus_mult(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("1-2*3;"))
        want = Node(
            NodeType.EXPR_BINARY,
            [
                BinaryOp.MINUS,
                Node(NodeType.INT_ATOM, 1),
                Node(
                    NodeType.EXPR_BINARY,
                    [
                        BinaryOp.MULT,
                        Node(NodeType.INT_ATOM, 2),
                        Node(NodeType.INT_ATOM, 3),
                    ],
                ),
            ],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)

    def test_parser_mult_minus(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("1*2-3;"))
        want = Node(
            NodeType.EXPR_BINARY,
            [
                BinaryOp.MINUS,
                Node(
                    NodeType.EXPR_BINARY,
                    [
                        BinaryOp.MULT,
                        Node(NodeType.INT_ATOM, 1),
                        Node(NodeType.INT_ATOM, 2),
                    ],
                ),
                Node(NodeType.INT_ATOM, 3),
            ],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)

    def test_parser_parens(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("(10/3);"))
        want = Node(
            NodeType.EXPR_BINARY,
            [BinaryOp.DIV, Node(NodeType.INT_ATOM, 10), Node(NodeType.INT_ATOM, 3)],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)

    def test_parser_parens_add(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("(10+3);"))
        want = Node(
            NodeType.EXPR_BINARY,
            [BinaryOp.PLUS, Node(NodeType.INT_ATOM, 10), Node(NodeType.INT_ATOM, 3)],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)

    def test_parser_parens_multi(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("(10/3) * 2;"))
        want = Node(
            NodeType.EXPR_BINARY,
            [
                BinaryOp.MULT,
                Node(
                    NodeType.EXPR_BINARY,
                    [
                        BinaryOp.DIV,
                        Node(NodeType.INT_ATOM, 10),
                        Node(NodeType.INT_ATOM, 3),
                    ],
                ),
                Node(NodeType.INT_ATOM, 2),
            ],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)

    def test_parens_override_precedence(self):
        from parser import Parser
        from lexer import Lexer

        parser = Parser(Lexer("(10+3) * 2;"))
        want = Node(
            NodeType.EXPR_BINARY,
            [
                BinaryOp.MULT,
                Node(
                    NodeType.EXPR_BINARY,
                    [
                        BinaryOp.PLUS,
                        Node(NodeType.INT_ATOM, 10),
                        Node(NodeType.INT_ATOM, 3),
                    ],
                ),
                Node(NodeType.INT_ATOM, 2),
            ],
        )
        got = parser.get_next_node()
        self.assertEqual(got, want)


if __name__ == "__main__":
    unittest.main()
