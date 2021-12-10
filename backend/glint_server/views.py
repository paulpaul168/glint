from glint_server import app


@app.get("/")
def home():
    print(app.config)
    a = {"message": "Hi from home", "god": app.config["GOD"]}
    return a
