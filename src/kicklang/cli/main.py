import typer
from rich import print
from rich.panel import Panel
from rich.tree import Tree
from pathlib import Path
from ..compiler.lexer import Lexer
from ..compiler.parser import Parser
from ..compiler.ast import Program

app = typer.Typer()

@app.command()
def compile(
    file: Path = typer.Argument(..., exists=True, dir_okay=False, help="The KickLang source file")
):
    """
    Compile a KickLang file to AST.
    """
    with open(file, "r", encoding="utf-8") as f:
        source = f.read()

    print(Panel(f"Compiling {file}", style="bold blue"))

    lexer = Lexer(source)
    parser = Parser(lexer)
    program = parser.parse_program()
    
    if parser.errors:
        print("[bold red]Parsing Errors:[/bold red]")
        for err in parser.errors:
            print(f" - {err}")
        raise typer.Exit(code=1)

    print("[bold green]Parsing Successful![/bold green]")
    print(program.model_dump_json(indent=2))

@app.command()
def run(
    file: Path = typer.Argument(..., exists=True, dir_okay=False)
):
    """
    Simulate running a KickLang file (Parsed & Validated).
    """
    compile(file)
    print("\n[bold yellow]Execution Simulation:[/bold yellow]")
    print("Interpreter not fully implemented. AST generated successfully.")

if __name__ == "__main__":
    app()
