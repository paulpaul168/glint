import os
from glint_server.linter_collection.exceptions import LintError
from glint_server.linter_collection.python import lint_python_project


def lint_project(path: str) -> dict:
    langs = _detect_languages(path)

    # TODO catch errors while linting
    result = {
        "status": "done",
        "linters": [],
        "files": [],
    }

    try:
        for lang in langs:
            lint = None
            if lang == "python":
                lint = lint_python_project(path)

            result["linters"] += lint["linters"]
            result["files"] += lint["files"]
    except LintError as e:
        return lint_project_error(e.message)

    return result


def lint_project_processing(path: str) -> dict:
    """The temporary result while the linting process is still ongoing."""
    return {
        "status": "processing",
        "files": [],
    }


def lint_project_error(error_msg: str) -> dict:
    """The result when an error occurred during linting."""
    return {
        "status": error_msg,
        "files": [],
    }


def _detect_languages(path: str) -> set[str]:
    extensions = {
        ".py": "python",
    }

    languages = set()
    for _, _, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)[1]
            if extension in extensions:
                languages.add(extensions[extension])

    return languages
