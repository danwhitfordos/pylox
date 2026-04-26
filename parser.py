from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Any

from lexer import Lexer, TokenType


class NodeType(IntEnum):
    INT_ATOM = auto()
    EXPR_BINARY = auto()

class BinaryOp(IntEnum):
    PLUS = auto()

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

    def get_atom(self):
        return Node(
            NodeType.INT_ATOM,
            int(self.previous.value)
        )

    def get_expression(self):
        self.advance()
        if self.current.type == TokenType.SEMICOLON:
            return self.get_atom()
        elif self.current.type == TokenType.PLUS:
            l = self.get_atom()
            op = BinaryOp.PLUS
            self.advance()
            r = self.get_expression()
            return Node(NodeType.EXPR_BINARY, [op, l, r])
        else:
            raise Exception(f"Unexpected '{t}' parsing expression")
        

    def get_next_node(self):
        self.advance()
        if self.current.type == TokenType.EOF:
            return None
        return self.get_expression()
