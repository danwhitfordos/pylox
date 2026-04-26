from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

from lexer import Lexer

class StatementType(Enum):
    RETURN = auto()
    INT_ATOM = auto()

@dataclass
class Statement():
    type: StatementType
    value: Any = None

class Parser():
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def get_atom(self):
        t = self.lexer.get_next_token()

    def get_expression(self):
        self.get_atom()
        self.consume_expected(TokenType.SEMICOLON)

    def get_next_statement(self):
        self.get_expression()
        return Statement(StatementType.RETURN)
