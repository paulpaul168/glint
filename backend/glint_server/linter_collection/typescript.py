import json
import subprocess
import tempfile
from typing import TextIO
from glint_server.linter_collection.javascript import normalize_eslint
from glint_server.linter_collection.exceptions import LintError


def lint_typescript_project(project_path: str, linter: str) -> dict:
    if linter == "eslint":
        return lint_eslint_typescript_project(project_path)
    else:
        raise LintError(f"Typescript linter '{linter}' is not known.")


def lint_eslint_typescript_project(project_path: str) -> dict:
    config_file = create_eslint_typescript_config()
    process = subprocess.run(
        [
            "eslint",
            "--config",
            config_file.name,
            "--format",
            "json",
            ".",
            "--ext",
            ".js",
        ],
        cwd=project_path,
        text=True,
        capture_output=True,
    )
    config_file.close()

    # Return an error if eslint crashed
    # https://eslint.org/docs/user-guide/command-line-interface#exit-codes
    if process.returncode == 2:
        print(process.stderr)
        raise LintError(f"ESLint returned with exit code {process.returncode}")

    eslint_res = json.loads(process.stdout)

    # Eslint also includes files without errors so we filter them here
    eslint_res = list(filter(lambda l: len(l["messages"]) > 0, eslint_res))

    # TODO: Maybe we should filter the eslint output so that we don't get
    # styleing stuff as this is almost never relevant during a CTF
    return normalize_eslint(eslint_res, project_path)


def create_eslint_typescript_config() -> TextIO:
    file = tempfile.NamedTemporaryFile(mode="w+")
    content = """
    {
        "env": {
            "browser": true,
            "es2021": true,
            "node": true
        },
        "extends": [
            "eslint:recommended",
            "plugin:@typescript-eslint/recommended"
        ],
        "parser": "@typescript-eslint/parser",
        "parserOptions": {
            "ecmaVersion": 13,
            "sourceType": "module"
        },
        "plugins": [
            "@typescript-eslint"
        ],
        "rules": {
        }
    } 
    """
    file.write(content)
    return file
