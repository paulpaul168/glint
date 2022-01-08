import os
import subprocess
import json
from pathlib import PurePath

from glint_server.linter_collection.exceptions import LintError


def lint_c_project(path: str, linter: str):
    if linter == "cpplint":
        return lint_c_project(path)
    else:
        raise LintError(f"C/C++ linter '{linter}' is not known.")


def lint_c_project(project_path: str):
    files = find_c_files(project_path)
    if files == []:
        return normalize_cpplint([])

    process = subprocess.run(
        ["cpplint"] + files,
        text=True,
        capture_output=True,
    )

    cpplint_res = process.stdout.split("\n")
    return normalize_cpplint(cpplint_res, project_path)


def normalize_cpplint(results: list[dict], project_path) -> dict:
    files = dict()

    for result in results:
        result_array = result.split("\t")
        if len(result_array) != 5:
            continue

        path = PurePath(result[0].split(":")[0]).relative_to(project_path).as_posix()

        if path not in files:
            files[path] = {
                "path": path,
                "name": os.path.basename(path),
                "linter": "cpplint",
                "lints": [],
            }

        lint = {
            "line": result[0].split(":")[1],
            "endLine": None,
            "column": None,
            "endColumn": None,
            "header": result[1],
            "message": result[2],
            "url": None,
        }

        files[path]["lints"].append(lint)

    return {
        "status": "done",
        "linters": {"c": "cpplint"},
        "files": list(files.values()),
    }


def find_c_files(path: str) -> list[str]:
    c_files = []
    for root, _, files in os.walk(path):
        for name in files:
            name = os.path.join(root, name)
            if os.path.splitext(name)[1][1:] in [
                "c",
                "c++",
                "cc",
                "cpp",
                "cu",
                "cuh",
                "cxx",
                "h",
                "h++",
                "hh",
                "hpp",
                "hxx",
            ]:
                c_files.append(name)

    return c_files
