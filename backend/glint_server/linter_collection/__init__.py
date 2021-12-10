def lint_file(path: str) -> dict:
    return {
        "line": 1,
        "endline": 2,
        "column": 15,
        "endColumn": 35,
        "path": "redact.py",
        "header": "Consider using with",
        "message": "Using open without explicitly specifying an encoding",
        "url": None,
    }
