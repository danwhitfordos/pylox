from enum import Enum, auto
from dataclasses import dataclass
import sys
from typing import Any

class TokenType(Enum):
    EOF = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    INTEGER = auto()
    LB = auto()
    RB = auto()
    SEMICOLON = auto()

@dataclass
class Token():
    type: TokenType
    value: Any = None

class Lexer():
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def advance(self, expected):
        cc = self.text[self.pos]
        if cc != expected:
            raise Exception("Advancing past unexpected token")
        self.pos += 1        

    def current_char(self) -> str | None:
        if self.pos >= len(self.text):
            return None
        cc = self.text[self.pos]
        self.pos += 1
        return cc
    
    def peek(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def get_next_token(self):
        c: str | None = self.current_char()
        if c is None:
            return Token(TokenType.EOF)
        
        while c.isspace():
            c = self.current_char()
            if c is None:
                return Token(TokenType.EOF)

        if c == '+':
            return Token(TokenType.PLUS)
        elif c == '-':
            return Token(TokenType.MINUS)
        elif c == '*':
            return Token(TokenType.MUL)
        elif c == '/':
            return Token(TokenType.DIV)
        elif c == '(':
            return Token(TokenType.LB)
        elif c == ')':
            return Token(TokenType.RB)
        elif c == ';':
            return Token(TokenType.SEMICOLON)
        elif c.isnumeric():
            return self.read_int(c)
        
        raise Exception(f"Unknown token: {c}")

    def read_int(self, lexeme: str):
        while True:
            c = self.peek()
            if c is None:
                return Token(TokenType.INTEGER, int(lexeme))
            if c.isnumeric():
                self.advance(c)
                lexeme += c
            else:
                return Token(TokenType.INTEGER, int(lexeme))

