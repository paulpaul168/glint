import os
from typing import Any
from glint_server.linter_collection.exceptions import LintError
from glint_server.linter_collection.javascript import lint_javascript_project
from glint_server.linter_collection.python import lint_python_project
from glint_server.linter_collection.go import lint_go_project


def get_supported_linters() -> dict[str, list[str]]:
    return {
        "python": ["pylint"],
        "go": ["staticcheck"],
        "javascript": ["eslint"],
    }


def lint_project(path: str, linters: dict[str, str]) -> dict:
    langs = _detect_languages(path)

    result = {
        "status": "done",
        "linters": dict(),
        "files": [],
    }

    try:
        for lang in langs:
            lint = None
            if lang == "python":
                lint = lint_python_project(path, linters)
            elif lang == "go":
                lint = lint_go_project(path, linters)
            elif lang == "javascript":
                lint = lint_javascript_project(path, linters)

            if lang not in result["linters"]:
                result["linters"].update(lint["linters"])

            result["files"] += lint["files"]
    except LintError as e:
        return lint_project_error(e.message)

    return result


def lint_project_processing(path: str) -> dict[str, Any]:
    """The temporary result while the linting process is still ongoing."""
    return {
        "status": "processing",
        "files": [],
    }


def lint_project_error(error_msg: str) -> dict[str, Any]:
    """The result when an error occurred during linting."""
    return {
        "status": error_msg,
        "files": [],
    }


def _detect_languages(path: str) -> set[str]:
    extensions = {
        ".py": "python",
        ".go": "go",
        ".js": "javascript",
    }

    languages = set()
    for _, _, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)[1]
            if extension in extensions:
                languages.add(extensions[extension])

    return languages
