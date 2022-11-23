from flask import Flask, render_template
import sqlalchemy
import json
import os

app = Flask(__name__)

posts = []
for postTitle in os.listdir("posts/"):
    posts.append(postTitle.rsplit(".", 1)[0])


@app.route("/")
def index():
    return render_template("index.html", title=posts)


@app.route("/<postID>")
def post(postID):
    if postID in posts:
        post = open("posts/%s.json" % (postID))
    else:
        return render_template("404.html", post=postID)
    data = json.load(post)
    return render_template(
        "post.html",
        title=data["title"],
        date=data["date"],
        author=data["author"],
        content=data["content"],
    )


if __name__ == "__main__":
    app.run(debug=True)
