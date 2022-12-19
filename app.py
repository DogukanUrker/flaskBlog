from flask import Flask, render_template, request, redirect
from wtforms import Form, PasswordField, StringField, validators

# Debugging
# print("\x1b[6;30;42m" + " SUCCESS " + "\x1b[0m")
# print("\x1b[6;30;41m" + " ERROR " + "\x1b[0m")

app = Flask(__name__)


class registerForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25)],
        render_kw={"placeholder": "username"},
    )
    email = StringField(
        "Email", [validators.Length(min=6, max=50)], render_kw={"placeholder": "email"}
    )
    password = PasswordField(
        "Passowrd", [validators.Length(min=8)], render_kw={"placeholder": "password"}
    )


class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25)],
        render_kw={"placeholder": "username"},
    )
    password = PasswordField(
        "Passowrd", [validators.Length(min=8)], render_kw={"placeholder": "password"}
    )


@app.route("/")
def index():
    return render_template(
        "index.html",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm(request.form)
    if request.method == "POST":
        userName = request.form["userName"]
        password = request.form["password"]
    return render_template("login.html", form=form, user=user)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = registerForm(request.form)
    if request.method == "POST":
        return redirect("/")
    return render_template("signup.html", form=form)


@app.route("/createpost")
def createPost():
    return render_template(
        "createPost.html",
    )


@app.route("/<postID>")
def post(postID):
    return postID


if __name__ == "__main__":
    app.run(debug=True)
