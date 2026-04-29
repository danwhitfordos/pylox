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
    DIV = auto()


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
        assert self.current is not None, "Unexpected end of input"
        if self.current.type == TokenType.LB:
            self.advance()
            expr = self.get_expression()
            assert self.current.type == TokenType.RB, "Expected closing parenthesis"
            self.advance()
            return expr
        else:
            self.advance()
            assert self.previous is not None, "Expected integer atom"
            return Node(NodeType.INT_ATOM, int(self.previous.value))

    def get_term(self) -> Node:
        assert self.current is not None
        l = self.get_factor()

        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            self.advance()
            assert self.previous is not None
            op = (
                BinaryOp.PLUS
                if self.previous.type == TokenType.PLUS
                else BinaryOp.MINUS
            )
            r = self.get_factor()
            l = Node(NodeType.EXPR_BINARY, [op, l, r])

        return l

    def get_factor(self) -> Node:
        assert self.current is not None
        l = self.get_atom()

        while self.current.type in (TokenType.MULT, TokenType.DIV):
            self.advance()
            assert self.previous is not None
            op = BinaryOp.MULT if self.previous.type == TokenType.MULT else BinaryOp.DIV
            r = self.get_atom()
            l = Node(NodeType.EXPR_BINARY, [op, l, r])

        return l

    def get_expression(self) -> Node:
        assert self.current is not None
        return self.get_term()

    def get_next_node(self) -> Node | None:
        self.advance()
        assert self.current is not None
        if self.current.type == TokenType.EOF:
            return None
        expr = self.get_expression()
        assert self.current.type == TokenType.SEMICOLON, (
            f"Expected semicolon got {self.current}"
        )
        return expr
