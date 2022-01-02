import os
import subprocess
import json
from pathlib import PurePath

from glint_server.linter_collection.exceptions import LintError


def lint_python_project(path: str, linter: str):
    print(linter)
    if linter == "bandit" or linter == "auto":
        return lint_bandit_project(path)
    elif linter == "pylint":
        return lint_pylint_project(path)
    else:
        raise LintError(f"Python linter '{linter}' is not known.")


def lint_pylint_project(project_path: str):
    # TODO: maybe there should be special treatment for packages 🤷‍♂️
    files = find_python_files(project_path)
    if files == []:
        return normalize_pylint([])

    process = subprocess.run(
        ["python3", "-m", "pylint", "--output-format=json", "--jobs=0"]
        + files,
        text=True,
        capture_output=True,
    )

    # Pylint return codes are weired but here is the official documentation
    # explaining it:
    # https://pylint.pycqa.org/en/latest/user_guide/run.html#exit-codes
    if process.returncode & 32 == 32:
        print(process.args)
        print(process.stdout)
        raise LintError(
            f"Pylint returned with usage error {process.returncode}"
        )

    if process.returncode & 1 == 1:
        print(process.stderr)
        raise LintError(
            f"Pylint returned with a fatal error {process.returncode}"
        )

    pylint_res = json.loads(process.stdout)
    # TODO: Maybe we should filter the pylint output so that we don't get
    # styleing stuff as this is almost never relevant during a CTF
    return normalize_pylint(pylint_res, project_path)


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


def lint_bandit_project(project_path: str) -> dict:
    process = subprocess.run(
        ["bandit", "-r", "-f", "json", "."],
        cwd=project_path,
        text=True,
        capture_output=True,
    )

    # Bandit doesn't indicate with exit codes if an error occoured so we need to
    # parse the json first
    report = json.loads(process.stdout)

    if len(report["errors"]) > 0:
        print(report["errors"])
        raise LintError("Bandit returned with errors")

    return normalize_bandit(report["results"], project_path)


def normalize_bandit(results: list[dict], project_path: str) -> dict:
    files = dict()

    for result in results:
        path = result["filename"]

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "bandit",
                "lints": [],
            }

        # TODO: should we add the severity to the header?
        lint = {
            "line": result["line_number"],
            "endLine": result["line_range"][-1],
            "column": result["col_offset"],
            "endColumn": None,
            "header": result["test_name"].replace("_", " ").capitalize(),
            "message": result["issue_text"],
            "url": result["more_info"],
        }
        files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"python": "bandit"},
        "files": list(files.values()),
    }


def find_python_files(path: str) -> list[str]:
    python_files = []
    for root, _, files in os.walk(path):
        for name in files:
            name = os.path.join(root, name)
            if os.path.splitext(name)[1] == ".py":
                python_files.append(name)

    return python_files
