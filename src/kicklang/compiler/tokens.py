from enum import Enum, auto
from typing import Optional
from pydantic import BaseModel

class TokenType(Enum):
    # Special
    EOF = auto()
    ERROR = auto()
    
    # Directives
    DIRECTIVE_ROLE = auto()    # ⫻role
    DIRECTIVE_MODULE = auto()  # ⫻module
    DIRECTIVE_IMPORT = auto()  # ⫻import
    DIRECTIVE_PATTERN = auto() # ⫻pattern
    DIRECTIVE_OUTPUT = auto()  # ⫻output
    
    # Keywords
    PLAN = auto()
    FIND = auto()
    SUMMARIZE = auto()
    LINK = auto()
    MAP = auto()
    CLUSTER = auto()
    COMPARE = auto()
    EXPLAIN = auto()
    DETAIL = auto()
    IF = auto()
    ELSE = auto()
    
    # Symbols
    ARROW = auto()             # →
    PIPE_START = auto()        # <<
    PIPE_END = auto()          # >>
    COLON = auto()             # :
    COMMA = auto()             # ,
    PLUS = auto()              # +
    MINUS = auto()             # -
    STAR = auto()              # *
    EQUALS = auto()            # =
    GT = auto()                # >
    LT = auto()                # <
    SEMICOLON = auto()         # ;
    
    # Identifiers & Literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    
    # Structure
    INDENT = auto()
    DEDENT = auto()
    
    # Relations (Special case for graph edges if they aren't just identifiers)
    # keeping as identifiers for now but might need specific types later
    
    NEWLINE = auto()

class Token(BaseModel):
    type: TokenType
    literal: str
    line: int
    column: int
    error_msg: Optional[str] = None

    def __str__(self):
        return f"Token({self.type.name}, '{self.literal}', {self.line}:{self.column})"
