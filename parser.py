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

    def advance(self):
        t = self.lexer.get_next_token()
        self.previous = t
        return t

    def get_atom(self):
        return Node(
            NodeType.INT_ATOM,
            int(self.previous.value)
        )

    def get_expression(self):
        t = self.lexer.get_next_token()
        if t.type == TokenType.SEMICOLON:
            return self.get_atom()
        elif t.type == TokenType.PLUS:
            l = self.get_atom()
            op = BinaryOp.PLUS
            self.previous = self.lexer.get_next_token()
            r = self.get_expression()
            return Node(NodeType.EXPR_BINARY, [op, l, r])
        else:
            raise Exception(f"Unexpected '{t}' parsing expression")
        

    def get_next_node(self):
        self.advance()
        if self.previous.type == TokenType.EOF:
            return None
        return self.get_expression()
