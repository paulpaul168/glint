from glint_server.linter_collection import lint_project
from glint_server.file import save_file
import urllib, threading


def do_lint(language: str, project_id: str) -> None:
    x = threading.Thread(target=lint_thread, args=(language, project_id))
    x.start()


def lint_thread(language: str, project_id: str) -> None:
    if language == "python":
        save_file(
            project_id + "/lint", str(lint_project(urllib.parse.unquote(project_id)))
        )
