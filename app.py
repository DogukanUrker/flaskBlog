from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

theme = "dark"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", theme=theme)


@app.route("/login")
def login():
    return render_template("login.html", theme=theme)


@app.route("/signup")
def signup():
    return render_template("signup.html", theme=theme)


@app.route("/createpost")
def createPost():
    return render_template("createPost.html", theme=theme)


@app.route("/<postID>")
def post(postID):
    return "post will be display here"


if __name__ == "__main__":
    app.run(debug=True)
