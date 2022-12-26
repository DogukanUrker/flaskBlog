from flask import Flask, render_template, request, redirect, flash
import sqlite3
from sqlite3 import Error
from wtforms import Form, PasswordField, StringField, validators
import secrets
from cryptography.fernet import Fernet


# Debugging
# print("\x1b[6;30;42m" + " SUCCESS " + "\x1b[0m")
# print("\x1b[6;30;41m" + " ERROR " + "\x1b[0m")

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

key = Fernet.generate_key()
f = Fernet(key)


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
    return "..."


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = registerForm(request.form)
    if request.method == "POST":
        userName = request.form["userName"]
        email = request.form["email"]
        password = f.encrypt(request.form["password"].encode("utf-8"))
        conn = sqlite3.connect("db/users.db")
        cur = conn.cursor()
        cur.execute(
            f'INSERT INTO  users(userName,email,password,role) VALUES("{userName}","{email}","{password}","user")'
        )
        conn.commit()
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
