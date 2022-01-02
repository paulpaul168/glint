import os
import subprocess
import json
from pathlib import PurePath

from glint_server.linter_collection.exceptions import LintError


def lint_python_project(path: str, linter: str):
    if linter == "pylint" or linter == "auto":
        return lint_pylint_project(path)
    else:
        raise LintError(f"Python linter '{linter}' is not known.")


def lint_pylint_project(project_path: str):
    # TODO: maybe there should be special treatment for packages 🤷‍♂️
    files = find_python_files(project_path)
    if files == []:
        return normalize_pylint([])

    process = subprocess.run(
        ["python3", "-m", "pylint", "--output-format=json", "--jobs=0"] + files,
        text=True,
        capture_output=True,
    )

    # Pylint return codes are weired but here is the official documentation
    # explaining it:
    # https://pylint.pycqa.org/en/latest/user_guide/run.html#exit-codes
    if process.returncode & 32 == 32:
        print(process.args)
        print(process.stdout)
        raise LintError(f"Pylint returned with usage error {process.returncode}")

    if process.returncode & 1 == 1:
        print(process.stderr)
        raise LintError(f"Pylint returned with a fatal error {process.returncode}")

    pylint_res = json.loads(process.stdout)
    # TODO: Maybe we should filter the pylint output so that we don't get
    # styleing stuff as this is almost never relevant during a CTF
    return normalize_pylint(pylint_res, project_path)


def find_python_files(path: str) -> list[str]:
    python_files = []
    for root, _, files in os.walk(path):
        for name in files:
            name = os.path.join(root, name)
            if os.path.splitext(name)[1] == ".py":
                python_files.append(name)

    return python_files


def normalize_pylint(results: list[dict], project_path) -> dict:
    files = dict()

    for result in results:
        path = PurePath(result["path"]).relative_to(project_path).as_posix()

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "pylint",
                "lints": [],
            }

        lint = {
            "line": result["line"],
            "endLine": result["endLine"],
            "column": result["column"],
            "endColumn": result["endColumn"],
            "header": result["symbol"].replace("-", " ").capitalize(),
            "message": result["message"],
            "url": f"https://vald-phoenix.github.io/pylint-errors/plerr/errors/imports/{result['message-id']}.html",
        }

        files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"python": "pylint"},
        "files": list(files.values()),
    }
