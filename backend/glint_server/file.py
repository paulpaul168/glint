from glint_server import app
import os
import urllib.parse


def create_project_folder(name: str) -> str:
    path = app.config["LINT_DIR"] + name
    if not os.path.exists(path):
        os.makedirs(
            path
        )  # comment this out to test frontend/backend connection without writing folders everywhere
    return path


def save_file(file_name: str, content: str):
<<<<<<< HEAD
    print(urllib.parse.unquote(file_name))
    # return # I have this in here to test frontend/backend connection without writing files everywhere
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(urllib.parse.unquote(file_name), "w+") as f:
=======
    # return # I have this in here to test frontend/backend connection without writing files everywhere
    with open(urllib.parse.unquote(file_name), "w") as f:
>>>>>>> 14fd1537e8a53f966d0144b2ec934bcc24717776
        f.write(content)
