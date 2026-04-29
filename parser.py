from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Any

from lexer import Lexer, TokenType, Token


class NodeType(IntEnum):
    INT_ATOM = auto()
    EXPR_BINARY = auto()


class BinaryOp(IntEnum):
    PLUS = auto()
    MINUS = auto()
    MULT = auto()


@dataclass
class Node:
    type: NodeType
    value: Any = None


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.previous = None
        self.current = None

    def advance(self):
        self.previous = self.current
        self.current = self.lexer.get_next_token()

    def get_atom(self) -> Node:
        assert self.current is not None, {
            "previous": self.previous,
            "current": self.current,
        }
        assert self.current.type == TokenType.INTEGER, {
            "previous": self.previous,
            "current": self.current,
        }
        self.advance()
        assert self.previous is not None
        return Node(NodeType.INT_ATOM, int(self.previous.value))

    def get_plus_minus(self) -> Node:
        assert self.current is not None
        l = self.get_mult_div()

        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current.type == TokenType.PLUS:
                self.advance()
                op = BinaryOp.PLUS
                r = self.get_mult_div()
                l = Node(NodeType.EXPR_BINARY, [op, l, r])
            elif self.current.type == TokenType.MINUS:
                self.advance()
                op = BinaryOp.MINUS
                r = self.get_mult_div()
                l = Node(NodeType.EXPR_BINARY, [op, l, r])

        return l
            

    def get_mult_div(self) -> Node:
        assert self.current is not None
        l = self.get_atom()

        if self.current.type == TokenType.MULT:
            self.advance()
            op = BinaryOp.MULT
            r = self.get_atom()
            return Node(NodeType.EXPR_BINARY, [op, l, r])
        else:
            return l

    def get_expression(self) -> Node:
        assert self.current is not None
        expr = self.get_plus_minus()
        assert self.current.type == TokenType.SEMICOLON, {
            "previous": self.previous,
            "current": self.current,
        }
        return expr

    def get_next_node(self) -> Node | None:
        self.advance()
        assert self.current is not None
        if self.current.type == TokenType.EOF:
            return None
        return self.get_expression()
