from glint_server import app
from flask import json, request
import urllib.parse

from glint_server.linter_collection import lint_project
from glint_server.file import save_file, create_project


@app.get("/")
def home():
    data = {
        "status": "OK",
        "version": "0.0.1",
    }
    return prepareResponse(data)


@app.post("/api/projects")
def create_project():
    post_content = request.json
    project_path = str(create_project(post_content["name"]))
    for file in post_content["files"]:
        save_file(file["path"], file["content"])
        print(file)
    project_path = urllib.parse.quote(project_path)
    data = {
        "name": post_content["name"],
        "projectId": project_path,
        "projectUrl": app.config["HOST"] + "/api/projects/" + project_path,
        "sourcesUrl": app.config["HOST"]
        + "/api/projects/"
        + project_path
        + "/sources",
        "lintUrl": app.config["HOST"]
        + "/api/projects/"
        + project_path
        + "/lint",
    }
    return prepareResponse(data)


@app.get("/api/projects/<project_id>/lint")
def get_lint(project_id):
    lint_result = lint_project(urllib.parse.unquote(project_id))
    return prepareResponse(lint_result)


def prepareResponse(jsonData: json):
    resp = app.response_class(
        response=json.dumps(jsonData), mimetype="application/json"
    )
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
