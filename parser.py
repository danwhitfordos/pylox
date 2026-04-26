from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from lexer import Lexer, TokenType

class NodeType(Enum):
    INT_ATOM = auto()

@dataclass
class Node():
    type: NodeType
    value: Any = None


class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def get_next_node(self):
        t = self.lexer.get_next_token()
        if t.type == TokenType.EOF:
            return None
        elif t.type == TokenType.INTEGER:
            return Node(NodeType.INT_ATOM, t.value)

