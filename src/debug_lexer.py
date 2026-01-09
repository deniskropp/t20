from pathlib import Path
from kicklang.compiler.lexer import Lexer
from kicklang.compiler.tokens import TokenType

def debug_tokens(file_path):
    print(f"Tokenizing {file_path}")
    with open(file_path, "r") as f:
        source = f.read()
    
    lexer = Lexer(source)
    count = 0
    while True:
        token = lexer.next_token()
        print(token)
        if token.type == TokenType.EOF:
            break
        if token.type == TokenType.ERROR:
             print("ERROR FOUND")
             break
        count += 1
        if count > 1000:
             print("BREAKING: Too many tokens")
             break

if __name__ == "__main__":
    debug_tokens("../examples/test.klang")
