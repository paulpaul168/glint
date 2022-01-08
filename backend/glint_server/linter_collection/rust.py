import json
import os
import subprocess

from glint_server.linter_collection.exceptions import LintError


def lint_rust_project(path: str, linter: str):
    if linter == "clippy":
        return lint_clippy_project(path)
    else:
        raise LintError(f"Rust linter '{linter}' is not known.")


def lint_clippy_project(project_path: str) -> dict:
    process = subprocess.run(
        ["cargo", "clippy", "--message-format", "json"],
        cwd=project_path,
        text=True,
        capture_output=True,
    )

    if process.returncode != 0:
        print(process.stderr)
        raise LintError(f"Clippy returned with exit code {process.returncode}")

    # Clippy produces json line format instead of json
    clippy_res = []
    for line in process.stdout.splitlines():
        clippy_res.append(json.loads(line))

    print(process.returncode)
    print(json.dumps(clippy_res))
    return normalize_clippy(clippy_res, project_path)


def normalize_clippy(results: list[dict], project_path: str) -> dict:
    files = dict()

    for result in results:
        if (
            result["reason"] != "compiler-message"
            or not result["message"]["spans"]
        ):
            continue

        # TODO: always first?
        span = result["message"]["spans"][0]
        path = span["file_name"]

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "clippy",
                "lints": [],
            }

        url = None
        for child in result["message"]["children"]:
            if "https://" in child["message"]:
                url = child["message"].split(" ")[-1]

        lint = {
            "line": span["line_start"],
            "endLine": span["line_end"],
            "column": span["column_start"],
            "endColumn": span["column_end"],
            "header": result["message"]["level"],
            "message": result["message"]["message"],
            "url": url,
        }

        files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"rust": "clippy"},
        "files": list(files.values()),
    }
