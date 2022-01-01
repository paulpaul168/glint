from glint_server import app
from glint_server.linter_collection import lint_project_error
import os, json, urllib.parse, shutil


def create_project_folder(name: str) -> str:
    path = app.config["LINT_DIR"] + name
    path_modifier = 0
    if os.path.exists(path):
        while os.path.exists(path + str(path_modifier)):
            path_modifier += 1
        os.makedirs(path + str(path_modifier))
        project_id = name + str(path_modifier)
    else:
        os.makedirs(path)
        project_id = name
    return project_id


def delete_project_folder(id: str) -> tuple[str, str]:
    path = app.config["LINT_DIR"] + id
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        return "OK", 200
    else:
        return "Project not found", 404


def delete_file(project_id: str, file_id: str) -> tuple[str, str]:
    path = app.config["LINT_DIR"] + project_id + "/" + file_id
    if os.path.exists(path):
        if not os.path.isfile(path):
            return "Not a file (directory?)", 501
        os.remove(path)
        return "OK", 200
    else:
        return "File not found", 404


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
