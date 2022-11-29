from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

theme = "dark"
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app)


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    posts = db.Column(db.String)
    password = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


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
