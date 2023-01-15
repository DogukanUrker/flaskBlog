import secrets
import sqlite3
from datetime import datetime
from passlib.hash import sha256_crypt
from forms import createPostForm, signUpForm, loginForm
from flask import Flask, render_template, redirect, flash, request, session


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config["SESSION_PERMANENT"] = True


def addPoints(points, userSession):
    conn = sqlite3.connect("db/users.db")
    cur = conn.cursor()
    cur.execute(
        f'UPDATE users set points = points+{points} where userName = "{userSession}"'
    )
    conn.commit()
    print(
        "\n"
        + "\x1b[6;30;42m"
        + f" {points} POINTS ADDED TO {userSession} "
        + "\x1b[0m"
        + "\n"
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "userName" in session:
        print("\n" + "\x1b[6;30;41m" + " USER ALREADY LOGGED IN " + "\x1b[0m" + "\n")
        return redirect("/")
    else:
        form = signUpForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            email = request.form["email"]
            password = request.form["password"]
            passwordConfirm = request.form["passwordConfirm"]
            if passwordConfirm == password:
                password = sha256_crypt.hash(password)
                conn = sqlite3.connect("db/users.db")
                cur = conn.cursor()
                cur.execute(
                    f"""
                    INSERT INTO  users(userName,email,password,role,points,creationDate,creationTime) 
                    VALUES("{userName}","{email}","{password}","user",0,
                    "{datetime.now().strftime("%d.%m.%y")}",
                    "{datetime.now().strftime("%H:%M")}")
                    """
                )
                conn.commit()
                print(
                    "\n"
                    + "\x1b[6;30;42m"
                    + " NEW USER ADDED TO DATABASE "
                    + "\x1b[0m"
                    + "\n"
                )
                return redirect("/")
            elif passwordConfirm != password:
                print(
                    "\n" + "\x1b[6;30;41m" + " PASSWORDS MUST MATCH " + "\x1b[0m" + "\n"
                )
                flash("password must match", "error")
        return render_template("signup.html", form=form, hideSignUp=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "userName" in session:
        print("\n" + "\x1b[6;30;41m" + " USER ALREADY LOGGED IN " + "\x1b[0m" + "\n")
        return redirect("/")
    else:
        form = loginForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            password = request.form["password"]
            conn = sqlite3.connect("db/users.db")
            cur = conn.cursor()
            cur.execute(f'SELECT * from users WHERE userName = "{userName}"')
            user = cur.fetchone()
            if not user:
                print("\n" + "\x1b[6;30;41m" + " USER NOT FOUND " + "\x1b[0m" + "\n")
                flash("user not found", "error")
            else:
                if sha256_crypt.verify(password, user[3]):
                    session["userName"] = userName
                    addPoints(1, session["userName"])
                    print("\n" + "\x1b[6;30;42m" + " USER FOUND " + "\x1b[0m" + "\n")
                    flash("user found", "success")
                    return redirect("/")
                else:
                    print(
                        "\n" + "\x1b[6;30;41m" + " WRONG PASSWORD " + "\x1b[0m" + "\n"
                    )
                    flash("wrong  password", "error")
        return render_template("login.html", form=form, hideLogin=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
                INSERT INTO posts(title,tags,content,author,views,date,time) 
                VALUES("{postTitle}","{postTags}","{postContent}",
                "{session["userName"]}",0,
                "{datetime.now().strftime("%d.%m.%y")}",
                "{datetime.now().strftime("%H:%M")}")
                """
            )
            conn.commit()
            print("\n" + "\x1b[6;30;42m" + " POSTED " + "\x1b[0m" + "\n")
            addPoints(10, session["userName"])
            return redirect("/")
        return render_template("createPost.html", form=form)
    else:
        print("\n" + "\x1b[6;30;41m" + " USER NOT LOGGED IN " + "\x1b[0m" + "\n")
        flash("you need login for create a post", "error")
        return redirect("/login")


@app.route("/<postID>", methods=["GET", "POST"])
def post(postID):
    conn = sqlite3.connect("db/posts.db")
    cur = conn.cursor()
    cur.execute(f"SELECT id from posts")
    posts = str(cur.fetchone())
    if postID in posts:
        print("\n" + "\x1b[6;30;42m" + " POST FOUNDED " + "\x1b[0m" + "\n")
        conn = sqlite3.connect("db/posts.db")
        cur = conn.cursor()
        cur.execute(f'SELECT * from posts WHERE id = "{postID}"')
        post = cur.fetchone()
        return render_template(
            "post.html",
            id=post[0],
            title=post[1],
            tags=post[2],
            content=post[3],
            views=post[4],
            author=post[5],
            date=post[6],
        )
    else:
        print("\n" + "\x1b[6;30;41m" + " 404 " + "\x1b[0m" + "\n")
        return render_template("404.html", notFound=postID)


if __name__ == "__main__":
    app.run(debug=True)


# Debugging
# print("\x1b[6;30;42m" + " SUCCESS " + "\x1b[0m")
# print("\x1b[6;30;41m" + " ERROR " + "\x1b[0m")
