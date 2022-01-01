from werkzeug.wrappers import response
from glint_server import app
from flask import json, request

from glint_server.linter_collection import lint_project_error
import glint_server.file as gfile
from glint_server.threading import do_lint
import os, urllib.parse

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
    for project_id in gfile.list_dirs():
        project_name = gfile.load_file(project_id + "/metadata.glint")["name"]
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
    return prepareResponse(data)


@app.get("/api/projects/<project_id>")
def get_project_content(project_id):
    data, error_code = gfile.get_project_files(project_id)
    return prepareResponse(data), error_code


@app.delete("/api/projects/<project_id>")
def delete_project(project_id):
    status, error_code = gfile.delete_project_folder(project_id)
    data = {
        "status": status,
    }
    return prepareResponse(data), error_code


@app.delete("/api/projects/<project_id>/sources/<path:file_id>")
def delete_file(project_id, file_id):
    status, error_code = gfile.delete_file(project_id, file_id)
    data = {
        "status": status,
    }
    return prepareResponse(data), error_code


@app.put("/api/projects/<project_id>/sources/<path:file_id>")
def upload_file(project_id, file_id):
    content = request.json["content"]
    data = {
        "status": "Not implemented",
    }
    error_code = 501
    return prepareResponse(data), error_code


@app.post("/api/projects/<project_id>/sources")
def new_source_file(project_id):
    request_data = request.json
    file_url = os.path.join(project_id, request_data["path"], request_data["fileName"])
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
    error_code = 200
    return prepareResponse(data), error_code


@app.patch("/api/projects/<project_id>")
def change_linter(project_id):
    request_data = request.json
    if request_data["name"] != None:
        metadata = gfile.load_file(project_id + "/metadata.glint")
        metadata["name"] = request_data["name"]
        gfile.save_file(project_id + "/metadata.glint", json.dumps(metadata))
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
    lint_result = gfile.load_file(project_id + "/lint.glint")
    return prepareResponse(lint_result)


def prepareResponse(jsonData: json):
    resp = app.response_class(
        response=json.dumps(jsonData), mimetype="application/json"
    )
    return resp
