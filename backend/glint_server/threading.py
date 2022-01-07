from glint_server.linter_collection import lint_project
from glint_server.file import save_file
from glint_server import app
import urllib, threading, json
import glint_server.file as gfile
from glint_server.linter_collection.lint import lint_project_processing


def do_lint(project_id: str, linters: dict) -> None:
    gfile.save_file(
        project_id + "/lint.glint",
        json.dumps(lint_project_processing(project_id, linters)),
    )
    thread = threading.Thread(
        target=lint_thread,
        args=(
            project_id,
            linters,
        ),
    )
    thread.start()


def lint_thread(project_id: str, linters: dict) -> None:
    save_file(
        project_id + "/lint.glint",
        json.dumps(
            lint_project(
                app.config["LINT_DIR"] + urllib.parse.unquote(project_id),
                linters,
            )
        ),
    )
