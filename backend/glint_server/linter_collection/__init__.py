from glint_server.linter_collection.python import lint_python_project


def lint_project(path: str) -> dict:
    # langs = _detect_languages(path)

    return lint_python_project(path)

    # return {
    #     "files": [
    #         {
    #             "name": "redact.py",
    #             "path": "/tmp/abc/redact.py",
    #             "lints": [
    #                 {
    #                     "line": 1,
    #                     "endLine": 2,
    #                     "column": 15,
    #                     "endColumn": 35,
    #                     "header": "Consider using with",
    #                     "message": "Using open without explicitly specifying an encoding",
    #                     "url": None,
    #                 },
    #             ],
    #         }
    #     ],
    # }


def _detect_languages(path: str) -> list[str]:
    # TODO: Actuall implementation
    return ["python"]


class LintException(Exception):
    pass
