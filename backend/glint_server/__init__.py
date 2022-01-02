import toml
from flask import Flask


app = Flask(__name__, instance_relative_config=True)
app.config.from_file("config.toml", load=toml.load)


from glint_server import views
