from glint_server import app
from glint_server.linter_collection import lint_project_error
import os, json, urllib.parse


def create_project_folder(name: str) -> str:
    path = app.config["LINT_DIR"] + name
    if not os.path.exists(path):
        os.makedirs(
            path
        )  # comment this out to test frontend/backend connection without writing folders everywhere
    return name


def save_file(file_name: str, content: str) -> None:
    # return # I have this in here to test frontend/backend connection without writing files everywhere
    file_name = app.config["LINT_DIR"] + file_name
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(urllib.parse.unquote(file_name), "w+") as f:
        f.write(content)


def load_file(file_name: str) -> json:
    file_name = app.config["LINT_DIR"] + file_name
    if not os.path.exists(file_name):
        return lint_project_error("Project ID unkown")
    with open(urllib.parse.unquote(file_name), "r") as f:
        return json.loads(f.read())


def list_dirs() -> dict:
    path = app.config["LINT_DIR"]
    dirs = []
    for dir in os.listdir(path):
        dirs.append(dir)
    return dirs
