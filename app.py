from flask import Flask, render_template
import json
app = Flask(__name__)
f = open("articles.json")
data = json.load(f)
@app.route("/")
def index():
    return render_template("index.html",title=data["title"],date=data["date"],content=data["content"])

@app.route("/{{articleID}}")
def article():
    f = open("articles/article.json")
    data = json.load(f)
    return render_template("article.html",title=data["title"],date=data["date"],content=data["content"])


if __name__ == "__main__":
    app.run(debug=True)