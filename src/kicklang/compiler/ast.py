from typing import List, Optional, Union, Literal, ForwardRef
from pydantic import BaseModel, Field
from .tokens import TokenType

# Handle Forward Refs
Statement = ForwardRef('Statement')
Expression = ForwardRef('Expression')
Command = ForwardRef('Command')
IfStatement = ForwardRef('IfStatement')

class ASTNode(BaseModel):
    pass

class Expression(ASTNode):
    type: str = 'Expression'

class Identifier(Expression):
    type: Literal['identifier'] = 'identifier'
    value: str

class Directive(Expression):
    type: Literal['directive'] = 'directive'
    name: str 
    parameter: Optional[str] = None 

class LiteralValue(Expression):
    type: Literal['literal'] = 'literal'
    value: Union[str, int, float]
    kind: Literal['string', 'number']

class PipeVariable(Expression):
    type: Literal['pipe_variable'] = 'pipe_variable'
    name: str

class PipeExpression(Expression):
    pass

# We need a Union of Expressions for polymorphic fields
ExpressionUnion = Union[Identifier, Directive, LiteralValue, PipeVariable, PipeExpression]

class Statement(ASTNode):
    type: str = 'Statement'

class Command(Statement):
    type: Literal['command'] = 'command'
    subject: Optional[ExpressionUnion] = None 
    verb: TokenType 
    args: List[ExpressionUnion] = Field(default_factory=list)
    options: List[ExpressionUnion] = Field(default_factory=list) 
    output: Optional[ExpressionUnion] = None 
    
    block: Optional[List['StatementUnion']] = None

class IfStatement(Statement):
    type: Literal['if'] = 'if'
    condition: List[ExpressionUnion]
    then_block: List['StatementUnion']
    else_block: Optional[List['StatementUnion']] = None

StatementUnion = Union[Command, IfStatement]

class Program(ASTNode):
    statements: List[StatementUnion]
