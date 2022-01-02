from werkzeug.wrappers import response
from glint_server import app
from flask import json, request

from glint_server.linter_collection import lint_project_error, get_supported_linters
import glint_server.file as gfile
from glint_server.threading import do_lint
import os, urllib.parse


@app.get("/")
def home():
    data = {
        "status": "OK",
        "version": "0.0.1",
    }
    return data


@app.get("/api/projects")
def get_project_list():
    projects = []
    error_code = 200
    for project_id in gfile.list_dirs():
        project_name, error_code = gfile.load_file(project_id + "/metadata.glint")
        if error_code != 200:
            return project_name, error_code
        project_name = project_name["name"]
        project_data = {
            "name": project_name,
            "projectId": project_id,
            "projectUrl": app.config["HOST"] + "/api/projects/" + project_id,
            "sourcesUrl": app.config["HOST"]
            + "/api/projects/"
            + project_id
            + "/sources",
            "lintUrl": app.config["HOST"] + "/api/projects/" + project_id + "/lint",
        }
        projects.append(project_data)
    data = {"projects": [projects]}
    return data, error_code


@app.get("/api/projects/<project_id>")
def get_project_content(project_id):
    data, error_code = gfile.get_project_files(project_id)
    return data, error_code


@app.delete("/api/projects/<project_id>")
def delete_project(project_id):
    status, error_code = gfile.delete_project_folder(project_id)
    data = {
        "status": status,
    }
    return data, error_code


@app.delete("/api/projects/<project_id>/sources/<path:file_id>")
def delete_file(project_id, file_id):
    status, error_code = gfile.delete_file(project_id, file_id)
    data = {
        "status": status,
    }
    return data, error_code


@app.put("/api/projects/<project_id>/sources/<path:file_id>")
def upload_file(project_id, file_id):
    data = {
        "status": "OK",
    }
    error_code = 200
    request_data = request.json
    file_url = os.path.join(project_id, file_id)
    if not gfile.path_exists(file_url):
        error_code = 404
        data = {
            "status": "File does not exists",
        }
    gfile.save_file(file_url, request_data["content"])

    return data, error_code


@app.post("/api/projects/<project_id>/sources")
def new_source_file(project_id):
    request_data = request.json
    file_url = os.path.join(project_id, request_data["path"], request_data["fileName"])
    if not gfile.path_exists(project_id):
        return {"status": "Error Project not found"}, 404
    gfile.save_file(file_url, request_data["content"])
    data = {
        "fileName": request_data["fileName"],
        "fileUrl": "/api/projects/"
        + project_id
        + "/sources/"
        + urllib.parse.quote(
            os.path.join(request_data["path"], request_data["fileName"]), safe=""
        ),
    }
    return data


@app.patch("/api/projects/<project_id>")
def change_linter(project_id):
    error_code = 200
    request_data = request.json
    if request_data["name"] != None:
        metadata, error_code = gfile.load_file(project_id + "/metadata.glint")
        if error_code != 200:
            return metadata, error_code
        metadata["name"] = request_data["name"]
        gfile.save_file(project_id + "/metadata.glint", json.dumps(metadata))
    if request_data["linters"] != None:
        do_lint(project_id, request_data["linters"])
    data = {
        "status": "OK",
    }
    return data, error_code


@app.post("/api/projects")
def create_project():
    post_content = request.json
    project_name = post_content["name"]
    linters = post_content["linters"]

    project_id = str(gfile.create_project_folder(project_name))
    for file in post_content["files"]:
        gfile.save_file(project_id + "/" + file["path"], file["content"])
    data = {
        "name": project_name,
        "projectId": project_id,
        "projectUrl": app.config["HOST"] + "/api/projects/" + project_id,
        "sourcesUrl": app.config["HOST"] + "/api/projects/" + project_id + "/sources",
        "lintUrl": app.config["HOST"] + "/api/projects/" + project_id + "/lint",
    }

    gfile.save_file(
        project_id + "/lint.glint", json.dumps(lint_project_error("processing"))
    )
    gfile.save_file(project_id + "/metadata.glint", json.dumps({"name": project_name}))
    do_lint(project_id, linters)
    return data


@app.get("/api/projects/<project_id>/lint")
def get_lint(project_id):
    lint_result, error_code = gfile.load_file(project_id + "/lint.glint")
    return lint_result, error_code


@app.get("/api/linters")
def get_linters():
    return get_supported_linters()


@app.post("/api/searchPatterns")
def save_search_pattern():
    error_code = 200
    request_data = request.json
    if gfile.path_exists("patterns.glint"):
        patterns, error_code = gfile.load_file("patterns.glint")
        return patterns, error_code
    else:
        patterns = {}
    pattern_name = request_data["patternName"]
    name_modifier = 0
    pattern_id = pattern_name
    if pattern_id in patterns:
        while (pattern_id + str(name_modifier)) in patterns:
            name_modifier += 1
        pattern_id = pattern_name + str(name_modifier)
    pattern = {
        "patternName": pattern_name,
        "regex": request_data["regex"],
    }
    patterns[pattern_id] = pattern
    gfile.save_file("patterns.glint", json.dumps(patterns))
    return_pattern = {
        "patternName": pattern_name,
        "patternId": pattern_id,
        "regex": request_data["regex"],
    }
    return return_pattern, error_code


@app.put("/api/searchPatterns/<pattern_id>")
def update_search_pattern(pattern_id):
    if gfile.path_exists("patterns.glint"):
        patterns, error_code = gfile.load_file("patterns.glint")
        if error_code != 200:
            return patterns, error_code
    else:
        patterns = {}
    if not pattern_id in patterns:
        return {"status": "Pattern not found"}, 404
    regex = request.json["regex"]
    pattern_name = request.json["patternName"]
    if regex != None:
        patterns[pattern_id]["regex"] = regex
    if pattern_name != None:
        patterns[pattern_id]["patternName"] = pattern_name
    gfile.save_file("patterns.glint", json.dumps(patterns))

    return {"status": "OK"}, error_code


@app.get("/api/searchPatterns")
def get_patterns():
    patterns, error_code = gfile.load_file("patterns.glint")
    return patterns, error_code


@app.delete("/api/searchPatterns/<pattern_id>")
def delete_pattern(pattern_id):
    if gfile.path_exists("patterns.glint"):
        patterns, error_code = gfile.load_file("patterns.glint")
        if error_code != 200:
            return patterns, error_code
    else:
        return {"status": "patternId not found."}, 404
    if not pattern_id in patterns:
        return {"status": "Pattern not found"}, 404
    patterns.pop(pattern_id)
    gfile.save_file("patterns.glint", json.dumps(patterns))
    return {"status": "OK"}


# needed because browser sends "options" request to same link before sending POST to check if CORS is allowed and I don't see another way to respond to the OPTIONS http request (@app.options doesn't exist)
@app.after_request
def return_allow_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp
