from glint_server.secrets import default_secrets
from werkzeug.wrappers import response
from glint_server import app
from flask import json, request

from glint_server.linter_collection import get_supported_linters
import glint_server.file as gfile
from glint_server.threading import do_lint
import os, urllib.parse


@app.before_first_request
def before_first_request():
    if not gfile.path_exists(app.config["LINT_DIR"]):
        gfile.create_path(app.config["LINT_DIR"])

    gfile.save_file("patterns.glint", json.dumps(default_secrets()))


@app.get("/")
def home():
    return {
        "status": "OK",
        "version": "0.0.1",
    }


@app.get("/api/projects")
def get_project_list():
    projects = []
    for project_id in gfile.list_dirs():
        metadata, error_code = gfile.load_json_file(
            project_id + "/metadata.glint"
        )
        if error_code != 200:
            return metadata, error_code
        project_data = {
            "name": metadata["name"],
            "projectId": project_id,
            "projectUrl": app.config["HOST"] + "/api/projects/" + project_id,
            "sourcesUrl": app.config["HOST"]
            + "/api/projects/"
            + project_id
            + "/sources",
            "lintUrl": app.config["HOST"]
            + "/api/projects/"
            + project_id
            + "/lint",
        }
        projects.append(project_data)
    return {"projects": projects}


@app.get("/api/projects/<project_id>")
def get_project_content(project_id):
    return gfile.get_project_files(project_id)


@app.delete("/api/projects/<project_id>")
def delete_project(project_id):
    status, error_code = gfile.delete_project_folder(project_id)
    if error_code != 200:
        return status, error_code
    return {
        "status": status,
    }


@app.delete("/api/projects/<project_id>/sources/<path:file_id>")
def delete_file(project_id, file_id):
    status, error_code = gfile.delete_file(project_id, file_id)
    if error_code != 200:
        return status, error_code
    return {
        "status": status,
    }


@app.put("/api/projects/<project_id>/sources/<path:file_id>")
def upload_file(project_id, file_id):
    request_data = request.json
    if request_data["content"] is None and request_data["path"] is None:
        return {"status": "bad request"}, 400

    file_url = os.path.join(project_id, file_id)
    if not gfile.path_exists(file_url):
        data = {
            "status": "File does not exist",
        }
        return data, 404

    if request_data["path"] is not None:
        gfile.move_file(
            file_url, os.path.join(project_id, request_data["path"])
        )
    if request_data["content"] is not None:
        gfile.save_file(file_url, request_data["content"])
    return {
        "status": "OK",
    }


@app.post("/api/projects/<project_id>/sources")
def new_source_file(project_id):
    request_data = request.json
    file_path = os.path.join(project_id, request_data["filePath"])

    if not gfile.path_exists(project_id):
        return {"status": "Error Project not found"}, 404

    gfile.save_file(file_path, request_data["content"])
    data = {
        "filePath": file_path,
        "fileUrl": "/api/projects/"
        + project_id
        + "/sources/"
        + urllib.parse.quote(
            os.path.join(request_data["filePath"]),
            safe="",
        ),
    }
    return data


@app.patch("/api/projects/<project_id>")
def change_linter(project_id):
    if request.json["name"] is None and request.json["linters"] is None:
        return {"status": "Bad request."}, 400

    if request.json["name"] is not None:
        metadata, error_code = gfile.load_json_file(
            project_id + "/metadata.glint"
        )
        if error_code != 200:
            return metadata, error_code
        metadata["name"] = request.json["name"]
        gfile.save_file(project_id + "/metadata.glint", json.dumps(metadata))

    if request.json["linters"] is not None:
        do_lint(project_id, request.json["linters"])

    return {"status": "OK"}


@app.post("/api/projects")
def create_project():
    post_content = request.json
    project_name = post_content["name"]

    project_id = gfile.create_project_folder(project_name)

    if "zip" in post_content:
        gfile.save_zip(project_id + "/file.zip", post_content["zip"])
    else:
        for file in post_content["files"]:
            gfile.save_file(project_id + "/" + file["path"], file["content"])

    gfile.save_file(
        project_id + "/metadata.glint", json.dumps({"name": project_name})
    )
    do_lint(project_id, post_content["linters"])

    data = {
        "name": project_name,
        "projectId": project_id,
        "projectUrl": app.config["HOST"] + "/api/projects/" + project_id,
        "sourcesUrl": app.config["HOST"]
        + "/api/projects/"
        + project_id
        + "/sources",
        "lintUrl": app.config["HOST"]
        + "/api/projects/"
        + project_id
        + "/lint",
    }
    return data


@app.get("/api/projects/<project_id>/lint")
def get_lint(project_id):
    return gfile.load_json_file(project_id + "/lint.glint")


@app.get("/api/linters")
def get_linters():
    return get_supported_linters()


@app.post("/api/searchPatterns")
def save_search_pattern():
    if gfile.path_exists("patterns.glint"):
        patterns, error_code = gfile.load_json_file("patterns.glint")
        if error_code != 200:
            return patterns, error_code
    else:
        patterns = {}

    pattern_name = request.json["patternName"]
    name_modifier = 0
    pattern_id = pattern_name
    if pattern_id in patterns:
        while (pattern_id + str(name_modifier)) in patterns:
            name_modifier += 1
        pattern_id = pattern_name + str(name_modifier)

    pattern = {
        "patternName": pattern_name,
        "regex": request.json["regex"],
    }
    patterns[pattern_id] = pattern
    gfile.save_file("patterns.glint", json.dumps(patterns))
    return_pattern = {
        "patternId": pattern_id,
        "patternName": pattern_name,
        "regex": request.json["regex"],
    }
    return return_pattern


@app.put("/api/searchPatterns/<pattern_id>")
def update_search_pattern(pattern_id):
    patterns, error_code = gfile.load_json_file("patterns.glint")
    if error_code != 200:
        return patterns, error_code

    if not pattern_id in patterns:
        return {"status": "Pattern not found"}, 404

    regex = request.json["regex"]
    pattern_name = request.json["patternName"]
    if regex is not None:
        patterns[pattern_id]["regex"] = regex
    if pattern_name is not None:
        patterns[pattern_id]["patternName"] = pattern_name

    gfile.save_file("patterns.glint", json.dumps(patterns))
    return {"status": "OK"}


@app.get("/api/searchPatterns")
def get_patterns():
    return gfile.load_json_file("patterns.glint")


@app.delete("/api/searchPatterns/<pattern_id>")
def delete_pattern(pattern_id):
    if gfile.path_exists("patterns.glint"):
        patterns, error_code = gfile.load_json_file("patterns.glint")
        if error_code != 200:
            return patterns, error_code
    else:
        return {"status": "No Pattern found."}, 404

    if not pattern_id in patterns:
        return {"status": "Pattern not found."}, 404

    patterns.pop(pattern_id)
    gfile.save_file("patterns.glint", json.dumps(patterns))
    return {"status": "OK"}


# Needed because browser sends "options" request to same link before sending
# POST to check if CORS is allowed and I don't see another way to respond to
# the OPTIONS http request (@app.options doesn't exist)
@app.after_request
def return_allow_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers[
        "Access-Control-Allow-Methods"
    ] = "POST, GET, OPTIONS, DELETE, PUT, PATCH"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp
