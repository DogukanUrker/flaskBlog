import secrets
import sqlite3
from datetime import datetime
from passlib.hash import sha256_crypt
from wtforms import Form, PasswordField, StringField, TextAreaField, validators
from flask import Flask, render_template, redirect, flash, request, session

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config["SESSION_PERMANENT"] = True


class signUpForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    email = StringField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"placeholder": "email"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
            validators.EqualTo(
                fieldname="passwordConfirm", message="Passwords must match"
            ),
        ],
        render_kw={"placeholder": "password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
    )


class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=8), validators.InputRequired()],
        render_kw={"placeholder": "password"},
    )


class createPostForm(Form):
    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"placeholder": "post title"},
    )
    postTags = StringField(
        "Post Tags", [validators.InputRequired()], render_kw={"placeholder": "tags"}
    )
    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=50), validators.InputRequired()],
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "userName" in session:
        print("\x1b[6;30;41m" + " USER ALREADY LOGGED IN " + "\x1b[0m")
        return redirect("/")
    else:
        form = signUpForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            password = request.form["password"]
            conn = sqlite3.connect("db/users.db")
            cur = conn.cursor()
            cur.execute(f'SELECT * from users WHERE userName = "{userName}"')
            user = cur.fetchone()
            if not user:
                print("\x1b[6;30;41m" + " USER NOT FOUND " + "\x1b[0m")
                flash("user not found", "error")
            else:
                if sha256_crypt.verify(password, user[3]):
                    session["userName"] = userName
                    print("\x1b[6;30;42m" + " USER FOUND " + "\x1b[0m")
                    flash("user found", "success")
                    return redirect("/")
                else:
                    print("\x1b[6;30;41m" + " WRONG PASSWORD " + "\x1b[0m")
                    flash("wrong  password", "error")
        return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "userName" in session:
        print("\x1b[6;30;41m" + " USER ALREADY LOGGED IN " + "\x1b[0m")
        return redirect("/")
    else:
        form = signUpForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            email = request.form["email"]
            password = sha256_crypt.hash(request.form["password"])
            conn = sqlite3.connect("db/users.db")
            cur = conn.cursor()
            cur.execute(
                f"""INSERT INTO  users(userName,email,password,role) 
                VALUES("{userName}","{email}","{password}","user")"""
            )
            conn.commit()
            print("\x1b[6;30;42m" + " NEW USER ADDED TO DATABASE " + "\x1b[0m")
            return redirect("/")
        return render_template("signup.html", form=form)


@app.route("/createpost", methods=["GET", "POST"])
def createPost():
    if "userName" in session:
        form = createPostForm(request.form)
        if request.method == "POST":
            postTitle = request.form["postTitle"]
            postTags = request.form["postTags"]
            postContent = request.form["postContent"]
            conn = sqlite3.connect("db/posts.db")
            cur = conn.cursor()
            cur.execute(
                f"""
                INSERT INTO posts(postTitle,postTags,postContent,postAuthor,postDate,postTime) 
                VALUES("{postTitle}","{postTags}","{postContent}",
                "{session["userName"]}",
                "{datetime.now().strftime("%d.%m.%y")}",
                "{datetime.now().strftime("%H:%M")}")
                """
            )
            conn.commit()
            print("\x1b[6;30;42m" + " POSTED " + "\x1b[0m")
            return redirect("/")
        return render_template("createPost.html", form=form)
    else:
        print("\x1b[6;30;41m" + " USER NOT LOGGED IN " + "\x1b[0m")
        flash("you need login for create a post", "error")
        return redirect("/login")


@app.route("/<postID>")
def post(postID):
    return f"<h1>{postID}</h1>"


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


# Debugging
# print("\x1b[6;30;42m" + " SUCCESS " + "\x1b[0m")
# print("\x1b[6;30;41m" + " ERROR " + "\x1b[0m")
