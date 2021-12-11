def lint_project(path: str) -> dict:
    return {
        "files": [
            {
                "name": "redact.py",
                "path": "/tmp/abc/redact.py",
                "lints": [
                    {
                        "line": 1,
                        "endline": 2,
                        "column": 15,
                        "endColumn": 35,
                        "header": "Consider using with",
                        "message": "Using open without explicitly specifying an encoding",
                        "url": None,
                    },
                ],
            }
        ],
    }
