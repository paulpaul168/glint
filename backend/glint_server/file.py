from glint_server import app
import os, urllib.parse


def create_project(name: str) -> str:
    path = app.config["LINT_DIR"] + name
    os.mkdir(path)
    return path


def save_file(file_name: str, content: str):
    with open(urllib.parse.unquote(file_name), "w") as f:
        f.write(content)
