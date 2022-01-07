import os
import subprocess
import json
from pathlib import PurePath

from glint_server.linter_collection.exceptions import LintError


def lint_php_project(path: str, linter: str):
    if linter == "PHP_CodeSniffer":
        return lint_phpcs_project(path)
    else:
        raise LintError(f"Php linter '{linter}' is not known.")


def lint_phpcs_project(project_path: str):
    files = find_php_files(project_path)
    if files == []:
        return normalize_phpcs([])

    process = subprocess.run(
        ["php", "linter/PHP_CodeSniffer/bin/phpcs", "--report=json"] + files,
        text=True,
        capture_output=True,
    )

    phpcs_res = json.loads(process.stdout)
    return normalize_phpcs(phpcs_res, project_path)


def normalize_phpcs(results: list[dict], project_path) -> dict:
    files = dict()

    for result in results["files"]:
        path = PurePath(result).relative_to(project_path).as_posix()

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "phpcs",
                "lints": [],
            }
        for message in results["files"][result]["messages"]:
            lint = {
                "line": message["line"],
                "endLine": None,
                "column": message["column"],
                "endColumn": None,
                "header": message["source"].replace(".", " ").capitalize(),
                "message": message["message"],
                "url": None,
            }

            files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"php": "phpcs"},
        "files": list(files.values()),
    }


def find_php_files(path: str) -> list[str]:
    python_files = []
    for root, _, files in os.walk(path):
        for name in files:
            name = os.path.join(root, name)
            if os.path.splitext(name)[1] == ".php":
                python_files.append(name)

    return python_files
