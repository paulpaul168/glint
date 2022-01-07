import json
import os
from pathlib import PurePath
import subprocess
from glint_server.linter_collection.exceptions import LintError


def lint_go_project(path: str, linter: str) -> dict:
    if linter == "gosec":
        return lint_gosec_project(path)
    elif linter == "staticcheck":
        return lint_staticcheck_project(path)
    else:
        raise LintError(f"Go linter '{linter}' is not known.")


def lint_staticcheck_project(project_path: str) -> dict:
    process = subprocess.run(
        ["staticcheck", "-f", "json"],
        cwd=project_path,
        text=True,
        capture_output=True,
    )

    # Staticcheck does not indicate with return codes if it failed or not so
    # we need to check the stderr output instead.
    if process.stderr != "":
        print(process.args)
        print(process.stderr)
        raise LintError(f"Staticcheck returned warning: {process.stderr}")

    # Staticcheck outputs not really json but json line format where each line
    # in the output is its own json object.
    staticcheck_res = []
    for line in process.stdout.splitlines():
        staticcheck_res.append(json.loads(line))

    # TODO: Maybe we should filter the staticcheck output so that we don't get
    # styleing stuff as this is almost never relevant during a CTF
    return normalize_staticcheck(staticcheck_res, project_path)


def normalize_staticcheck(results: list[dict], project_path: str) -> dict:
    files = dict()

    for result in results:
        path = (
            PurePath(result["location"]["file"])
            .relative_to(project_path)
            .as_posix()
        )

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "staticcheck",
                "lints": [],
            }

        lint = {
            "line": result["location"]["line"],
            "endLine": result["end"]["line"],
            "column": result["location"]["column"],
            "endColumn": result["end"]["column"],
            "header": result["severity"].capitalize()
            + " "
            + result["code"],  # TODO: find a better header
            "message": result["message"],
            "url": f"https://staticcheck.io/docs/checks/#{result['code']}",
        }

        files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"go": "staticcheck"},
        "files": list(files.values()),
    }


def lint_gosec_project(project_path: str) -> dict:
    process = subprocess.run(
        ["gosec", "-fmt", "json", "."],
        cwd=project_path,
        text=True,
        capture_output=True,
    )

    # TODO: there doesn't seam to be a way to see if gosec failed
    report = json.loads(process.stdout)

    return normalize_gosec(report["Issues"], project_path)


def normalize_gosec(results: list[dict], project_path: str) -> dict:
    files = dict()

    for result in results:
        path = PurePath(result["file"]).relative_to(project_path).as_posix()

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "gosec",
                "lints": [],
            }

        lint = {
            "line": result["line"],
            "endLine": result["line"],
            "column": result["column"],
            "endColumn": None,
            "header": result["details"],
            "message": result["details"],
            "url": result["cwe"]["url"],
        }

        files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"go": "gosec"},
        "files": list(files.values()),
    }
