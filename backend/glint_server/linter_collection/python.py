import os
import subprocess
import json


def lint_python_project(path: str):
    # TODO: path is not actually what we want here, as pylint needs the name
    # of a module. Don't quite know how to solve that right now

    # TODO: check that path is only ever a path and that there is no
    # attack-surface
    process = subprocess.run(
        ["python3", "-m", "pylint", "--output-format=json", path],
        text=True,
        capture_output=True,
    )

    # Pylint return codes are weired but here is the official documentation
    # explaining it:
    # https://pylint.pycqa.org/en/latest/user_guide/run.html#exit-codes
    if process.returncode & 1 == 1:
        print(process.stderr)
        raise Exception(
            f"Pylint returned with a fatal error {process.returncode}"
        )

    pylint_res = json.loads(process.stdout)
    # TODO: Maybe we should filter the pylint output so that we don't get
    # styleing stuff as this is almost never relevant during a CTF
    return normalize_pylint(pylint_res)


def normalize_pylint(results: list[dict]) -> dict:
    files = dict()

    for result in results:
        path = result["path"]

        if path not in files:
            files[path] = {
                "path": result["path"],
                "name": os.path.basename(result["path"]),
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

    return {"files": list(files.values())}
