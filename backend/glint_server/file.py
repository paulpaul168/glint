from glint_server import app
import tempfile

def create_project(name: str) -> tempfile:
    return tempfile.TemporaryDirectory(suffix="_"+name,prefix=app.config["PREFIX"])