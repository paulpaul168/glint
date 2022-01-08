import os
from typing import Any
from glint_server.linter_collection.exceptions import LintError
from glint_server.linter_collection.javascript import lint_javascript_project
from glint_server.linter_collection.python import lint_python_project
from glint_server.linter_collection.go import lint_go_project
from glint_server.linter_collection.php import lint_php_project
from glint_server.linter_collection.rust import lint_rust_project


def get_supported_linters() -> dict[str, list[str]]:
    return {
        "go": ["gosec", "staticcheck"],
        "javascript": ["eslint"],
        "php": ["phpcs"],
        "python": ["bandit", "pylint"],
        "rust": ["clippy"],
    }


def get_auto_linter(lang: str) -> str:
    mapping = {
        "go": "gosec",
        "javascript": "eslint",
        "php": "phpcs",
        "python": "bandit",
        "rust": "clippy",
    }
    return mapping[lang]


def lint_project(path: str, linters: dict[str, str]) -> dict:
    langs = detect_languages(path)
    linters = get_linters(langs, linters)

    result = {
        "status": "done",
        "linters": linters,
        "files": [],
    }

    try:
        for lang in langs:
            linter = linters[lang]

            lint = None
            if lang == "go":
                lint = lint_go_project(path, linter)
            elif lang == "javascript":
                lint = lint_javascript_project(path, linter)
            elif lang == "php":
                lint = lint_php_project(path, linter)
            elif lang == "python":
                lint = lint_python_project(path, linter)
            elif lang == "rust":
                lint = lint_rust_project(path, linter)

            if lang not in result["linters"]:
                result["linters"].update(lint["linters"])

            result["files"] += lint["files"]
    except LintError as e:
        return lint_project_error(path, linters, e.message)

    return result


def get_linters(
    langs: set[str], linter_prefs: dict[str, str]
) -> dict[str, str]:
    linters = dict()

    # We make a new set to avoid modifying the passed reference
    target_langs = set(langs)
    target_langs.update(linter_prefs.keys())
    for lang in target_langs:
        if lang in linter_prefs and linter_prefs[lang] != "auto":
            linters[lang] = linter_prefs[lang]
        else:
            linters[lang] = get_auto_linter(lang)

    return linters


def lint_project_processing(
    path: str, linter_prefs: dict[str, str]
) -> dict[str, Any]:
    """The temporary result while the linting process is still ongoing."""

    return lint_project_error(path, linter_prefs, "processing")


def lint_project_error(
    path: str, linter_prefs: dict[str, str], error_msg: str
) -> dict[str, Any]:
    """The result when an error occurred during linting."""

    langs = detect_languages(path)
    linters = get_linters(langs, linter_prefs)

    return {
        "status": error_msg,
        "linters": linters,
        "files": [],
    }


def lint_project_error_short(error_msg: str) -> dict[str, Any]:
    """The result when an error and we don't even know the project yet"""

    return {
        "status": error_msg,
        "linters": {},
        "files": [],
    }


def detect_languages(path: str) -> set[str]:
    extensions = {
        ".go": "go",
        ".js": "javascript",
        ".php": "php",
        ".py": "python",
        ".rs": "rust",
    }

    languages = set()
    for _, _, files in os.walk(path):
        for name in files:
            extension = os.path.splitext(name)[1]
            if extension in extensions:
                languages.add(extensions[extension])

    return languages
