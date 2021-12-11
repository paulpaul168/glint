from glint_server import app
from glint_server import file
from flask import json

from glint_server.linter_collection import lint_file


@app.get("/")
def home():
    a = {
        "message": "Hi from home",
        "god": app.config["GOD"],
        "tempfile": str(file.create_project("Test")),
    }
    a = lint_file("abc")
    resp = app.response_class(response=json.dumps(a), mimetype="application/json")
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp
