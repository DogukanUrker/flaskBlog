from flask import Flask, render_template, redirect
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
    try:
        post = open("posts/{}".format(postID))
    except:
        return redirect("/404")
    data = json.load(post)
    return render_template(
        "post.html", title=data["title"], date=data["date"], content=data["content"]
    )


@app.errorhandler(404)
def page_not_found():
    return "404", 404


if __name__ == "__main__":
    app.run(debug=True)
