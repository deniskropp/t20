from pathlib import Path
from kicklang.compiler.lexer import Lexer
from kicklang.compiler.parser import Parser

def debug_parser(file_path):
    print(f"Parsing {file_path}")
    with open(file_path, "r") as f:
        source = f.read()
    
    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    print("Parsing Done")
    print(f"Statements: {len(program.statements)}")

if __name__ == "__main__":
    debug_parser("../examples/test.klang")
