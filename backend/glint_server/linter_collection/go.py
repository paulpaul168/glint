import json
import os
import subprocess
from glint_server.linter_collection.exceptions import LintError


def lint_go_project(path: str, linters: dict[str, str]):
    if "go" not in linters:
        return lint_staticcheck_project(path)

    linter = linters["go"]
    if linter == "staticcheck":
        return lint_staticcheck_project(path)
    else:
        raise LintError(f"Go linter '{linter}' is not known.")


def lint_staticcheck_project(path: str):
    process = subprocess.run(
        ["staticcheck", "-f", "json"],
        cwd=path,
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
    return normalize_staticcheck(staticcheck_res)


def normalize_staticcheck(results: list[dict]) -> dict:
    files = dict()

    for result in results:
        path = result["location"]["file"]  # TODO: Make relative path

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
