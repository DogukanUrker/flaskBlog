import secrets
import sqlite3
from passlib.hash import sha256_crypt
from wtforms import Form, PasswordField, StringField, validators
from flask import Flask, render_template, redirect, flash, request, session


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)


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
    if "userName" in session:
        return render_template("index.html", logined=True, userName=session["userName"])
    else:
        return render_template("index.html", logined=False, userName="Guest")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = registerForm(request.form)
    if request.method == "POST":
        userName = request.form["userName"]
        password = request.form["password"]
        session["userName"] = userName
        conn = sqlite3.connect("db/users.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * from users WHERE userName = "{userName}"')
        user = cur.fetchone()
        if not user:
            print("\x1b[6;30;41m" + " USER NOT FOUND " + "\x1b[0m")
            flash("user not found", "error")
        else:
            if sha256_crypt.verify(password, user[3]):
                print("\x1b[6;30;42m" + " USER FOUND " + "\x1b[0m")
                flash("user found", "success")
                return redirect("/")
            else:
                print("\x1b[6;30;41m" + " WRONG PASSWORD " + "\x1b[0m")
                flash("wrong  password", "error")
    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = registerForm(request.form)
    if request.method == "POST":
        userName = request.form["userName"]
        email = request.form["email"]
        password = sha256_crypt.hash(request.form["password"])
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
    return f"<h1>{postID}</h1>"


if __name__ == "__main__":
    app.run(debug=True)


# Debugging
# print("\x1b[6;30;42m" + " SUCCESS " + "\x1b[0m")
# print("\x1b[6;30;41m" + " ERROR " + "\x1b[0m")
