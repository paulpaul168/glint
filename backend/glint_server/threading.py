from glint_server.linter_collection import lint_project
from glint_server.file import save_file
import urllib, threading, json


def do_lint(project_id: str) -> None:
    x = threading.Thread(target=lint_thread, args=(project_id,))
    x.start()


def lint_thread(project_id: str) -> None:
    save_file(
        project_id + "/lint",
        json.dumps(lint_project(urllib.parse.unquote(project_id))),
    )
