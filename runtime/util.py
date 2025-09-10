import os

def read_file(file_path: str) -> str:
    """Reads content from a given file path."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"Error reading file {file_path}: {e}"
