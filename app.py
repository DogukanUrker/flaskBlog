from flask import Flask, render_template,redirect
import json
import os
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html",title=os.listdir("posts/"))





@app.route("/<postID>")
def post(postID):
    try:
        f = open("posts/{}".format(postID))
    except:
        return redirect("/404")
    data = json.load(f)
    return render_template("post.html",title=data["title"],date=data["date"],content=data["content"])


@app.route("/404")
def page_not_found():
    return "404"



if __name__ == "__main__":
    app.run(debug=True)