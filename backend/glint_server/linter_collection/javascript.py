import json
import os
import subprocess
import tempfile
from typing import Any, TextIO

from glint_server.linter_collection.exceptions import LintError


def lint_javascript_project(path: str, linters: dict[str, str]) -> dict:
    if "javascript" not in linters:
        return lint_eslint_project(path)

    linter = linters["javascript"]
    if linter == "staticcheck" or linter == "auto":
        return lint_eslint_project(path)
    else:
        raise LintError(f"Javascript linter '{linter}' is not known.")


def lint_eslint_project(path: str) -> dict:
    config_file = create_eslint_config()
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
        cwd=path,
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
    return normalize_eslint(eslint_res)


def create_eslint_config() -> TextIO:
    file = tempfile.NamedTemporaryFile(mode="w+")
    content = """
    {
        "env": {
            "browser": true,
            "es2021": true,
            "node": true
        },
        "extends": "eslint:recommended",
        "parserOptions": {
            "ecmaVersion": 13,
            "sourceType": "module"
        },
        "rules": {
        }
    }
    """
    file.write(content)
    return file


def normalize_eslint(results: list[dict]) -> dict:
    files = dict()

    for result in results:
        path = result["filePath"]  # TODO: Make relative path

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "eslint",
                "lints": [],
            }

        for message in result["messages"]:
            lint = {
                "line": message["line"],
                "endLine": message["endLine"],
                "column": message["column"],
                "endColumn": message["endColumn"],
                "header": message["ruleId"].replace("-", " ").capitalize(),
                "message": message["message"],
                "url": f"https://eslint.org/docs/rules/{message['ruleId']}",
            }

            files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"javascript": "eslint"},
        "files": list(files.values()),
    }
