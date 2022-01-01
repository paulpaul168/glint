from werkzeug.wrappers import response
from glint_server import app
from flask import json, request

from glint_server.linter_collection import lint_project_error
from glint_server.file import save_file, create_project_folder, load_file, list_dirs
from glint_server.threading import do_lint

import time  # sometimes needed to test frontend behavior for slow answers


@app.get("/")
def home():
    data = {
        "status": "OK",
        "version": "0.0.1",
    }
    return prepareResponse(data)


@app.get("/api/projects")
def get_project_list():
    projects = []
    for dir in list_dirs():
        project_data = {"name": dir, "projectId": dir}
        projects.append(project_data)
    data = {"projects": [projects]}
    return prepareResponse(data)


@app.delete("/api/projects/<project_id>/sources/<file_id>")
def delete_file(project_id, file_id):
    data = {
        "status": "Not implemented",
    }
    error_code = 501
    return prepareResponse(data), error_code


@app.put("/api/projects/<project_id>/sources/<file_id>")
def upload_file(project_id, file_id):
    content = request.json["content"]
    data = {
        "status": "Not implemented",
    }
    error_code = 501
    return prepareResponse(data), error_code


@app.patch("/api/projects/<project_id>")
def change_linter(project_id):
    request_data = request.json
    if request_data["name"] != None:
        metadata = load_file(project_id + "/metadata.glint")
        metadata["name"] = request_data["name"]
        save_file(project_id + "/metadata.glint", metadata)
    if request_data["linters"] != None:
        do_lint(project_id, request_data["linters"])
    data = {
        "status": "OK",
    }
    error_code = 200
    return prepareResponse(data), error_code


@app.post("/api/projects")
def create_project():
    post_content = request.json
    project_name = post_content["name"]
    linters = post_content["linters"]

    project_id = str(create_project_folder(project_name))
    for file in post_content["files"]:
        save_file(project_id + "/" + file["path"], file["content"])
    data = {
        "name": project_name,
        "projectId": project_id,
        "projectUrl": app.config["HOST"] + "/api/projects/" + project_id,
        "sourcesUrl": app.config["HOST"] + "/api/projects/" + project_id + "/sources",
        "lintUrl": app.config["HOST"] + "/api/projects/" + project_id + "/lint",
    }

    save_file(project_id + "/lint.glint", json.dumps(lint_project_error("processing")))
    save_file(project_id + "/metadata.glint", {"name": project_name})
    do_lint(project_id, linters)
    return prepareResponse(data)


# needed because browser sends "options" request to same link before sending POST to check if CORS is allowed and I don't see another way to respond to the OPTIONS http request (@app.options doesn't exist)
@app.after_request
def return_allow_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.get("/api/projects/<project_id>/lint")
def get_lint(project_id):
    lint_result = load_file(project_id + "/lint.glint")
    return prepareResponse(lint_result)


def prepareResponse(jsonData: json):
    resp = app.response_class(
        response=json.dumps(jsonData), mimetype="application/json"
    )
    return resp
