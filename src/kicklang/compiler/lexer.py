from typing import List, Optional
from .tokens import Token, TokenType

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.position = 0
        self.read_position = 0
        self.ch: Optional[str] = None
        self.line = 1
        self.column = 0
        
        self.indent_stack = [0]
        self.pending_tokens: List[Token] = []
        
        self.read_char()

    def read_char(self):
        if self.read_position >= self.length:
            self.ch = None
        else:
            self.ch = self.source[self.read_position]
        
        self.position = self.read_position
        self.read_position += 1
        self.column += 1

    def peek_char(self) -> Optional[str]:
        if self.read_position >= self.length:
            return None
        return self.source[self.read_position]

    def next_token(self) -> Token:
        if self.pending_tokens:
            return self.pending_tokens.pop(0)

        # Skip spaces but NOT newlines yet, we need to handle them
        self.skip_inline_whitespace()

        if self.ch is None:
            # Check if we need to dedent remaining stack at EOF
            if len(self.indent_stack) > 1:
                self.indent_stack.pop()
                return Token(type=TokenType.DEDENT, literal="", line=self.line, column=self.column)
            return Token(type=TokenType.EOF, literal="", line=self.line, column=self.column)

        if self.ch == '\n':
            # Handle Indentation
            self.handle_newline()
            if self.pending_tokens:
                 return self.pending_tokens.pop(0)
            # If newline resulted in no tokens (e.g. blank line), recurse
            return self.next_token()

        token: Token
        
        # Extended Identifiers / Directives
        if self.ch == '⫻': # U+2AEB
            start_col = self.column
            literal = self.read_directive()
            token_type = self.lookup_directive(literal)
            return Token(type=token_type, literal=literal, line=self.line, column=start_col)

        if self.ch == '→': # U+2192
            token = Token(type=TokenType.ARROW, literal="→", line=self.line, column=self.column)
            self.read_char()
            return token
            
        if self.ch == '<':
            if self.peek_char() == '<':
                start_col = self.column
                self.read_char() # consume first <
                self.read_char() # consume second <
                return Token(type=TokenType.PIPE_START, literal="<<", line=self.line, column=start_col)
            else:
                token = Token(type=TokenType.LT, literal="<", line=self.line, column=self.column)
                self.read_char()
                return token
        
        if self.ch == '>':
            if self.peek_char() == '>':
                start_col = self.column
                self.read_char() # consume first >
                self.read_char() # consume second >
                return Token(type=TokenType.PIPE_END, literal=">>", line=self.line, column=start_col)
            else:
                token = Token(type=TokenType.GT, literal=">", line=self.line, column=self.column)
                self.read_char()
                return token

        if self.ch == ':':
            token = Token(type=TokenType.COLON, literal=":", line=self.line, column=self.column)
            self.read_char()
            return token
            
        if self.ch == ';':
            token = Token(type=TokenType.SEMICOLON, literal=";", line=self.line, column=self.column)
            self.read_char()
            return token
            
        if self.ch == '=':
            token = Token(type=TokenType.EQUALS, literal="=", line=self.line, column=self.column)
            self.read_char()
            return token
            
        if self.ch == ',':
            token = Token(type=TokenType.COMMA, literal=",", line=self.line, column=self.column)
            self.read_char()
            return token

        if self.ch == '+':
            token = Token(type=TokenType.PLUS, literal="+", line=self.line, column=self.column)
            self.read_char()
            return token
            
        if self.ch == '-':
            token = Token(type=TokenType.MINUS, literal="-", line=self.line, column=self.column)
            self.read_char()
            return token
            
        if self.ch == '*':
            token = Token(type=TokenType.STAR, literal="*", line=self.line, column=self.column)
            self.read_char()
            return token
            
        if self.ch == '"':
            start_col = self.column
            literal = self.read_string()
            return Token(type=TokenType.STRING, literal=literal, line=self.line, column=start_col)

        if self.is_letter_or_digit(self.ch):
            start_col = self.column
            literal = self.read_identifier()
            token_type = self.lookup_keyword(literal)
            return Token(type=token_type, literal=literal, line=self.line, column=start_col)

        # Unknown char
        token = Token(type=TokenType.ERROR, literal=self.ch, line=self.line, column=self.column, error_msg=f"Unexpected character: {self.ch}")
        self.read_char()
        return token

    def skip_inline_whitespace(self):
        while self.ch is not None and self.ch in [' ', '\t', '\r']:
            self.read_char()
            
    def handle_newline(self):
        # Consume the newline
        while self.ch == '\n':
            self.read_char()
            self.line += 1
            self.column = 0
            
        # Calculate indent of next line
        indent_len = 0
        while self.ch is not None and self.ch in [' ', '\t']:
            indent_len += 1
            self.read_char()
            
        if self.ch is None: 
            # EOF after newline
            return
            
        if self.ch == '\n':
            # Empty line with spaces, ignore
            self.handle_newline()
            return

        # Compare with stack
        current_indent = self.indent_stack[-1]
        
        if indent_len > current_indent:
            self.indent_stack.append(indent_len)
            self.pending_tokens.append(Token(type=TokenType.NEWLINE, literal="\n", line=self.line-1, column=0)) # Emit newline before indent? Usually yes.
            self.pending_tokens.append(Token(type=TokenType.INDENT, literal="", line=self.line, column=0))
        elif indent_len < current_indent:
            self.pending_tokens.append(Token(type=TokenType.NEWLINE, literal="\n", line=self.line-1, column=0))
            while indent_len < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.pending_tokens.append(Token(type=TokenType.DEDENT, literal="", line=self.line, column=0))
            if indent_len != self.indent_stack[-1]:
                # Error: inconsistent indentation
                 self.pending_tokens.append(Token(type=TokenType.ERROR, literal="", line=self.line, column=0, error_msg="Inconsistent indentation"))
        else:
             self.pending_tokens.append(Token(type=TokenType.NEWLINE, literal="\n", line=self.line-1, column=0))
             
    def read_string(self) -> str:
        # Assumes initial " is already peeking or current? 
        # Current char IS "
        self.read_char() # consume opening "
        start_pos = self.position
        while self.ch is not None and self.ch != '"':
            self.read_char()
        literal = self.source[start_pos:self.position]
        if self.ch == '"':
            self.read_char() # consume closing "
        return literal

    def read_identifier(self) -> str:
        start_pos = self.position
        while self.ch is not None and (self.is_letter_or_digit(self.ch) or self.ch in ['_', '.']):
             self.read_char()
        return self.source[start_pos:self.position]

    def read_directive(self) -> str:
        start_pos = self.position
        self.read_char() # consume ⫻
        while self.ch is not None and self.is_letter_or_digit(self.ch):
            self.read_char()
        return self.source[start_pos:self.position]

    def is_letter_or_digit(self, ch: str) -> bool:
        return ch.isalnum() or ch == '_'

    def lookup_keyword(self, literal: str) -> TokenType:
        keywords = {
            "PLAN": TokenType.PLAN,
            "FIND": TokenType.FIND,
            "SUMMARIZE": TokenType.SUMMARIZE,
            "LINK": TokenType.LINK,
            "MAP": TokenType.MAP,
            "CLUSTER": TokenType.CLUSTER,
            "COMPARE": TokenType.COMPARE,
            "EXPLAIN": TokenType.EXPLAIN,
            "DETAIL": TokenType.DETAIL,
            "IF": TokenType.IF,
            "ELSE": TokenType.ELSE
        }
        return keywords.get(literal, TokenType.IDENTIFIER)

    def lookup_directive(self, literal: str) -> TokenType:
        directives = {
            "⫻role": TokenType.DIRECTIVE_ROLE,
            "⫻module": TokenType.DIRECTIVE_MODULE,
            "⫻import": TokenType.DIRECTIVE_IMPORT,
            "⫻pattern": TokenType.DIRECTIVE_PATTERN,
            "⫻output": TokenType.DIRECTIVE_OUTPUT
        }
        
        base = directives.get(literal)
        if base: return base
        
        if literal.startswith("⫻"):
            pass
            
        return TokenType.IDENTIFIER
