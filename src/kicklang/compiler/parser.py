from typing import List, Optional
from .tokens import Token, TokenType
from .lexer import Lexer
from .ast import (
    Program, Statement, Command, IfStatement, 
    Expression, Identifier, Directive, LiteralValue, PipeVariable, ASTNode
)

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.cur_token: Token = self.lexer.next_token()
        self.peek_token: Token = self.lexer.next_token()
        self.errors: List[str] = []

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def cur_token_is(self, t: TokenType) -> bool:
        return self.cur_token.type == t

    def peek_token_is(self, t: TokenType) -> bool:
        return self.peek_token.type == t

    def parse_program(self) -> Program:
        statements = []
        while not self.cur_token_is(TokenType.EOF):
            # print(f"DEBUG: {self.cur_token}")
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            # If parse_statement returned None, it means it just consumed a Newline, so we are ready for next.
        return Program(statements=statements)

    def parse_statement(self) -> Optional[Statement]:
        if self.cur_token_is(TokenType.NEWLINE):
            self.next_token()
            return None
        
        if self.cur_token_is(TokenType.IF):
            return self.parse_if_statement()
            
        return self.parse_command_statement()

    def parse_command_statement(self) -> Statement:
        subject = None
        
        # 1. Parse Subject (Optional)
        # Strategy: Peek ahead.
        # Directives are definitely subjects (or standalone).
        # Identifiers could be subjects or verbs (if verb is implicit? No, explicit verbs).
        
        has_subject = False
        
        if self.cur_token.type == TokenType.DIRECTIVE_ROLE:
            subject = self.parse_expression() # Consumes directive
            has_subject = True
        elif self.cur_token.type == TokenType.IDENTIFIER:
            # Check if next is COLON or VERB
            if self.peek_token_is(TokenType.COLON):
                subject = self.parse_expression()
                self.next_token() # skip Colon
                has_subject = True
            elif self.is_verb(self.peek_token.type):
                subject = self.parse_expression()
                has_subject = True
            elif self.peek_token_is(TokenType.DIRECTIVE_ROLE): # e.g. Stage1 ⫻role...
                 # Maybe subject is Stage1?
                 subject = self.parse_expression()
                 has_subject = True

        verb = TokenType.IDENTIFIER # Default
        
        if self.is_verb(self.cur_token.type):
            verb = self.cur_token.type
            self.next_token() # Consume verb
        elif has_subject:
             # We parsed a subject, but current token is NOT a verb?
             # Check if we should default or error
             # e.g. `⫻role:Storyteller` alone on a line?
             # If newline next, it's a valid statement (just setting context?)
             # Spec doesn't imply that.
             pass
        else:
             # No subject, No verb.
             # If we are here, and didn't consume anything, we MUST ensure we consume something or error
             # otherwise infinite loop.
             if not self.is_end_of_statement(self.cur_token) and not self.cur_token_is(TokenType.ARROW): # Arrow handled in args
                 pass
             # If it is ARROW, we let Args loop handle it?
             pass

        # 3. Parse Args
        args = []
        output = None
        block = None
        
        while not self.is_end_of_statement(self.cur_token):
            if self.cur_token_is(TokenType.ARROW):
                self.next_token()
                output = self.parse_expression()
                # Assuming output is the last thing before newline/block
                break 
            
            if self.cur_token_is(TokenType.COMMA):
                self.next_token()
                continue
                
            arg = self.parse_expression()
            if arg:
                args.append(arg)
            else:
                # If parse_expression returned None but we aren't at end, force advance to avoid infinite loop
                # This catches things like unrelated tokens
                if not self.is_end_of_statement(self.cur_token):
                    # Error or skip
                    self.next_token()
            
        # 4. Check for Block (PLAN)
        if verb == TokenType.PLAN:
            # Plan statements might end with a block
            if self.cur_token_is(TokenType.NEWLINE):
                self.next_token()
            
            if self.cur_token_is(TokenType.INDENT):
                block = self.parse_block()

        return Command(subject=subject, verb=verb, args=args, output=output, block=block)

    def parse_if_statement(self) -> IfStatement:
        self.next_token() # skip IF
        condition = []
        while not self.cur_token_is(TokenType.COLON) and not self.cur_token_is(TokenType.NEWLINE) and not self.cur_token_is(TokenType.EOF):
            expr = self.parse_expression()
            if expr: condition.append(expr)
            else: self.next_token()
            
        if self.cur_token_is(TokenType.COLON):
            self.next_token()
            
        if self.cur_token_is(TokenType.NEWLINE):
            self.next_token()
            
        then_block = []
        if self.cur_token_is(TokenType.INDENT):
            then_block = self.parse_block()
        else:
            # Inline IF
            stmt = self.parse_command_statement()
            if stmt: then_block.append(stmt)
            
        else_block = None
        # Handle ELSE
        # If block parsed, we might be at a Newline or Dedent or the next line
        # If next line starts with ELSE
        # We need to be careful about newlines between Dedent and Else
        
        while self.cur_token_is(TokenType.NEWLINE):
            self.next_token()
            
        if self.cur_token_is(TokenType.ELSE):
            self.next_token() # skip ELSE
            if self.cur_token_is(TokenType.COLON): self.next_token()
            if self.cur_token_is(TokenType.NEWLINE): self.next_token()
            
            if self.cur_token_is(TokenType.INDENT):
                else_block = self.parse_block()
            else:
                 stmt = self.parse_command_statement()
                 if stmt: else_block = [stmt]
                 
        return IfStatement(condition=condition, then_block=then_block, else_block=else_block)

    def parse_block(self) -> List[Statement]:
        self.next_token() # consume INDENT
        statements = []
        while not self.cur_token_is(TokenType.DEDENT) and not self.cur_token_is(TokenType.EOF):
            if self.cur_token_is(TokenType.NEWLINE):
                self.next_token()
                continue
                
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
                
        if self.cur_token_is(TokenType.DEDENT):
            self.next_token()
            
        return statements

    def parse_expression(self) -> Optional[Expression]:
        # Consumes the tokens of the expression and points to the next token
        if self.cur_token_is(TokenType.IDENTIFIER):
            val = self.cur_token.literal
            self.next_token()
            return Identifier(value=val)
            
        if self.cur_token_is(TokenType.DIRECTIVE_ROLE) or self.cur_token_is(TokenType.DIRECTIVE_MODULE):
            return self.parse_directive()
            
        if self.cur_token_is(TokenType.STRING):
            val = self.cur_token.literal
            self.next_token()
            return LiteralValue(value=val, kind='string')
        if self.cur_token_is(TokenType.NUMBER):
            val = self.cur_token.literal
            self.next_token()
            return LiteralValue(value=val, kind='number')
            
        if self.cur_token_is(TokenType.PIPE_START):
            return self.parse_pipe_var()
            
        if self.cur_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.STAR]:
             val = self.cur_token.literal
             self.next_token()
             return Identifier(value=val)

        return None

    def parse_pipe_var(self):
        self.next_token() # skip <<
        val = ""
        while not self.cur_token_is(TokenType.PIPE_END) and not self.cur_token_is(TokenType.EOF):
            val += self.cur_token.literal
            self.next_token()
        
        if self.cur_token_is(TokenType.PIPE_END):
             self.next_token()
             
        return PipeVariable(name=val)

    def parse_directive(self):
        name = self.cur_token.literal
        self.next_token() # Consume directive name
        
        param = None
        if self.cur_token_is(TokenType.COLON):
            self.next_token() # skip colon
            if self.cur_token_is(TokenType.IDENTIFIER):
                param = self.cur_token.literal
                self.next_token() # consume param
                
        return Directive(name=name, parameter=param)

    def is_verb(self, t: TokenType) -> bool:
        return t in [
            TokenType.PLAN, TokenType.FIND, TokenType.SUMMARIZE, TokenType.LINK, 
            TokenType.MAP, TokenType.CLUSTER, TokenType.COMPARE, TokenType.EXPLAIN, 
            TokenType.DETAIL
        ]

    def is_end_of_statement(self, token: Token) -> bool:
        return token.type in [
            TokenType.NEWLINE, TokenType.EOF, TokenType.INDENT, TokenType.DEDENT
        ]
