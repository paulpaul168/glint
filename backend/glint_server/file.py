from glint_server import app
from glint_server.linter_collection import lint_project_error
import os, json, urllib.parse, shutil
from pathlib import PurePath


def path_exists(path: str) -> bool:
    return os.path.exists(os.path.join(app.config["LINT_DIR"], path))


def create_project_folder(name: str) -> str:
    path = os.path.join(app.config["LINT_DIR"], name)
    path_modifier = 0
    project_id = name
    if os.path.exists(path):
        while os.path.exists(path + str(path_modifier)):
            path_modifier += 1
        path = path + str(path_modifier)
        project_id = name + str(path_modifier)

    os.makedirs(path)

    return project_id


def delete_project_folder(id: str) -> tuple[str, str]:
    path = app.config["LINT_DIR"] + id
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
        return "OK", 200
    else:
        return "Project not found", 404


def delete_file(project_id: str, file_id: str) -> tuple[str, str]:
    path = os.path.join(app.config["LINT_DIR"], project_id, file_id)
    if os.path.exists(path):
        if not os.path.isfile(path):
            return "Not a file (directory?)", 400
        os.remove(path)
        return "OK", 200
    else:
        return "File not found", 404


def save_file(file_name: str, content: str) -> None:
    file_name = os.path.join(app.config["LINT_DIR"], file_name)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(urllib.parse.unquote(file_name), "w+") as f:
        f.write(content)


def load_json_file(file_name: str) -> tuple[dict, str]:
    file_name = os.path.join(app.config["LINT_DIR"], file_name)
    if not os.path.exists(file_name):
        return lint_project_error(file_name + " not found."), 404
    with open(urllib.parse.unquote(file_name), "r") as f:
        return json.loads(f.read()), 200


def get_project_files(project_id) -> tuple[dict, str]:
    path = os.path.join(app.config["LINT_DIR"], project_id)
    lint, error_code = load_json_file(project_id + "/lint.glint")
    if error_code != 200:
        return lint, error_code
    if lint["status"] != "done":
        return lint, 418  # TODO: hmm not sure if we are really a teapod here...

    found_files = []
    for root, _, files in os.walk(path):
        for name in files:
            if "glint" in os.path.splitext(name)[1]:
                continue

            with open(os.path.join(root, name)) as f:
                content = f.read()

            file_path = PurePath(os.path.join(path, name)).relative_to(path).as_posix()
            file = {
                "name": name,
                "path": file_path,
                "content": content,
            }
            found_files.append(file)

    linters = lint["linters"]
    metadata, error_code = load_json_file(project_id + "/metadata.glint")
    if error_code != 200:
        return metadata, error_code

    project_name = metadata["name"]
    output = {
        "name": project_name,
        "projectId": project_id,
        "files": found_files,
        "linters": linters,
    }
    return output


def list_dirs() -> dict:
    path = app.config["LINT_DIR"]
    dirs = []
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            dirs.append(dir)
    return dirs
