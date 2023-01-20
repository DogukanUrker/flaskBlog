import secrets
import sqlite3
from forms import *
from datetime import datetime
from passlib.hash import sha256_crypt
from flask import Flask, render_template, redirect, flash, request, session


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config["SESSION_PERMANENT"] = True


def message(color, message):
    print(
        f'\n\033[94m[{datetime.now().strftime("%d.%m.%y")}\033[0m'
        f'\033[95m {datetime.now().strftime("%H:%M:%S")}]\033[0m'
        f"\033[9{color}m {message}\033[0m\n"
    )


def addPoints(points, userSession):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'update users set points = points+{points} where userName = "{userSession}"'
    )
    connection.commit()
    message("2", f'{points} POINTS ADDED TO "{userSession}"')


@app.route("/")
def index():
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return render_template("index.html", posts=posts)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "userName" in session:
        message("1", f'"{session["userName"]}" ALREADY LOGGED IN')
        return redirect("/")
    else:
        form = signUpForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            email = request.form["email"]
            password = request.form["password"]
            passwordConfirm = request.form["passwordConfirm"]
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute("select userName from users")
            users = str(cursor.fetchall())
            cursor.execute("select email from users")
            mails = str(cursor.fetchall())
            if not userName in users and not email in mails:
                if passwordConfirm == password:
                    password = sha256_crypt.hash(password)
                    connection = sqlite3.connect("db/users.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f"""
                        insert into users(userName,email,password,role,points,creationDate,creationTime) 
                        values("{userName}","{email}","{password}","user",0,
                        "{datetime.now().strftime("%d.%m.%y")}",
                        "{datetime.now().strftime("%H:%M")}")
                        """
                    )
                    connection.commit()
                    message("2", f'"{userName}" ADDED TO DATABASE')
                    return redirect("/")
                elif passwordConfirm != password:
                    message("1", " PASSWORDS MUST MATCH ")
                    flash("password must match", "error")
            elif userName in users and email in mails:
                message("1", f'"{userName}" & "{email}" IS UNAVAILABLE ')
                flash("This username and email is unavailable.", "error")
            elif not userName in users and email in mails:
                message("1", f'THIS EMAIL "{email}" IS UNAVAILABLE ')
                flash("This email is unavailable.", "error")
            elif userName in users and not email in mails:
                message("1", f'THIS USERNAME "{userName}" IS UNAVAILABLE ')
                flash("This username is unavailable.", "error")
        return render_template("signup.html", form=form, hideSignUp=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if "userName" in session:
        message("1", f'"{session["userName"]}" ALREADY LOGGED IN')
        return redirect("/")
    else:
        form = loginForm(request.form)
        if request.method == "POST":
            userName = request.form["userName"]
            password = request.form["password"]
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(f'select * from users where userName = "{userName}"')
            user = cursor.fetchone()
            if not user:
                message("1", f'"{userName}" NOT FOUND')
                flash("user not found", "error")
            else:
                if sha256_crypt.verify(password, user[3]):
                    session["userName"] = userName
                    # addPoints(1, session["userName"])
                    message("2", f'"{userName}" LOGGED IN')
                    flash("user found", "success")
                    return redirect("/")
                else:
                    message("1", "WRONG PASSWORD")
                    flash("wrong  password", "error")
        return render_template("login.html", form=form, hideLogin=True)


@app.route("/logout")
def logout():
    if "userName" in session:
        message("2", f'"{session["userName"]}" LOGGED OUT')
        session.clear()
        return redirect("/")
    else:
        message("1", f"USER NOT LOGGED IN")
        return redirect("/")


@app.route("/createpost", methods=["GET", "POST"])
def createPost():
    if "userName" in session:
        form = createPostForm(request.form)
        if request.method == "POST":
            postTitle = request.form["postTitle"]
            postTags = request.form["postTags"]
            postContent = request.form["postContent"]
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(
                f"""
                instert into posts(title,tags,content,author,views,date,time) 
                values("{postTitle}","{postTags}","{postContent}",
                "{session["userName"]}",0,
                "{datetime.now().strftime("%d.%m.%y")}",
                "{datetime.now().strftime("%H:%M")}")
                """
            )
            connection.commit()
            message("2", f"'{postTitle}' POSTED")
            addPoints(10, session["userName"])
            return redirect("/")
        return render_template("createPost.html", form=form)
    else:
        message("1", "USER NOT LOGGED IN")
        flash("you need login for create a post", "error")
        return redirect("/login")


@app.route("/<postID>", methods=["GET", "POST"])
def post(postID):
    form = commentForm(request.form)
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute(f"select id from posts")
    posts = str(cursor.fetchall())
    if postID in posts:
        message("2", f'"{postID}" FOUND')
        connection = sqlite3.connect("db/posts.db")
        cursor = connection.cursor()
        cursor.execute(f'select * from posts where id = "{postID}"')
        post = cursor.fetchone()
        # cursor.execute(f'UPDATE posts set views = views+1 where id = "{postID}"')
        connection.commit()
        if request.method == "POST":
            comment = request.form["comment"]
            connection = sqlite3.connect("db/comments.db")
            cursor = connection.cursor()
            cursor.execute(
                f"""
                insert into comments(post,comment,user,date,time)
                values({postID},"{comment}","{session["userName"]}",
                "{datetime.now().strftime("%d.%m.%y")}",
                "{datetime.now().strftime("%H:%M")}")
                """
            )
            connection.commit()
        connection = sqlite3.connect("db/comments.db")
        cursor = connection.cursor()
        cursor.execute(f'select * from comments where post = "{postID}"')
        comments = cursor.fetchall()
        return render_template(
            "post.html",
            id=post[0],
            title=post[1],
            tags=post[2],
            content=post[3],
            views=post[4],
            author=post[5],
            date=post[6],
            form=form,
            comments=comments,
        )
    else:
        message("1", "404")
        return render_template("404.html", notFound=postID)


if __name__ == "__main__":
    app.run(debug=True)
