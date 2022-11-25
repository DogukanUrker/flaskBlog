from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import json
import os

theme = "dark"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskBlog.db"
db = SQLAlchemy(app)

""""
with app.app_context():
    db.create_all()

    db.session.add(User(username="example"))
    db.session.commit()

    users = db.session.execute(db.select(User)).scalars()
"""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)


posts = []
for postTitle in os.listdir("posts/"):
    posts.append(postTitle.rsplit(".", 1)[0])


@app.route("/")
def index():
    return render_template("index.html", title=posts, theme=theme)


@app.route("/<postID>")
def post(postID):
    if postID in posts:
        post = open("posts/%s.json" % (postID))
    else:
        return render_template("404.html", post=postID, theme=theme)
    data = json.load(post)
    return render_template(
        "post.html",
        title=data["title"],
        date=data["date"],
        author=data["author"],
        content=data["content"],
        theme=theme,
    )


if __name__ == "__main__":
    app.run(debug=True)
