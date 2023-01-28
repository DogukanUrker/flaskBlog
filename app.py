import os
import secrets
import sqlite3
from datetime import datetime
from passlib.hash import sha256_crypt
from forms import commentForm, loginForm, createPostForm, signUpForm, changePasswordForm
from flask import (
    Flask,
    request,
    session,
    flash,
    redirect,
    render_template,
    send_from_directory,
)


# import dbChecker

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config["SESSION_PERMANENT"] = True


def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime(seconds=False):
    match seconds:
        case False:
            return datetime.now().strftime("%H:%M")
        case True:
            return datetime.now().strftime("%H:%M:%S")


def message(color, message):
    print(
        f"\n\033[94m[{currentDate()}\033[0m"
        f"\033[95m {currentTime(True)}]\033[0m"
        f"\033[9{color}m {message}\033[0m\n"
    )
    logFile = open("log.log", "a")
    # logFile.write(f"[{currentDate()}" f"|{currentTime(True)}]" f" {message}\n")
    logFile.close()


def addPoints(points, userSession):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'update users set points = points+{points} where userName = "{userSession}"'
    )
    connection.commit()
    message("2", f'{points} POINTS ADDED TO "{userSession}"')


def getProfilePicture(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(f'select profilePicture from users where userName = "{userName}"')
    return cursor.fetchone()[0]


@app.context_processor
def utility_processor():
    def getProfilePicture(userName):
        connection = sqlite3.connect("db/users.db")
        cursor = connection.cursor()
        cursor.execute(
            f'select profilePicture from users where userName = "{userName}"'
        )
        return cursor.fetchone()[0]

    return dict(getProfilePicture=getProfilePicture)


@app.errorhandler(404)
def notFound(e):
    message("1", "404")
    return render_template("404.html"), 404


@app.route("/")
def index():
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return render_template(
        "index.html",
        posts=posts,
    )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    match "userName" in session:
        case True:
            message("1", f'"{session["userName"]}" ALREADY LOGGED IN')
            return redirect("/")
        case False:
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
                            insert into users(userName,email,password,profilePicture,role,points,creationDate,creationTime) 
                            values("{userName}","{email}","{password}","https://api.dicebear.com/5.x/identicon/svg?seed={secrets.token_urlsafe(32)}","user",0,
                            "{currentDate()}",
                            "{currentTime()}")
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
    match "userName" in session:
        case True:
            message("1", f'"{session["userName"]}" ALREADY LOGGED IN')
            return redirect("/")
        case False:
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
    match "userName" in session:
        case True:
            message("2", f'"{session["userName"]}" LOGGED OUT')
            session.clear()
            return redirect("/")
        case False:
            message("1", f"USER NOT LOGGED IN")
            return redirect("/")


@app.route("/createpost", methods=["GET", "POST"])
def createPost():
    match "userName" in session:
        case True:
            form = createPostForm(request.form)
            if request.method == "POST":
                postTitle = request.form["postTitle"]
                postTags = request.form["postTags"]
                postContent = request.form["postContent"]
                connection = sqlite3.connect("db/posts.db")
                cursor = connection.cursor()
                cursor.execute(
                    f"""
                    insert into posts(title,tags,content,author,views,date,time,lastEditDate,lastEditTime) 
                    values("{postTitle}","{postTags}","{postContent}",
                    "{session["userName"]}",0,
                    "{currentDate()}",
                    "{currentTime()}",
                    "{currentDate()}",
                    "{currentTime()}")
                    """
                )
                connection.commit()
                message("2", f'"{postTitle}" POSTED')
                addPoints(10, session["userName"])
                return redirect("/")
            return render_template("createPost.html", form=form)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need loin for create a post", "error")
            return redirect("/login")


@app.route("/deletepost/<int:postID>")
def deletePost(postID):
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f"select author from posts where id = {postID}")
            author = cursor.fetchone()
            match author[0] == session["userName"]:
                case True:
                    cursor.execute(f"delete from posts where id = {postID}")
                    connection.commit()
                    message("2", f'"{postID}" DELETED')
                    return redirect("/")
                case False:
                    message(
                        "1",
                        f'"{postID}" NOT DELETED "{postID}" DOES NOT BELONG TO {session["userName"]}',
                    )
                    return redirect("/")
        case False:
            message("1", f'USER NEEDS TO LOGIN FOR DELETE "{postID}"')
            return redirect("/")


@app.route("/changepassword", methods=["GET", "POST"])
def changePassword():
    match "userName" in session:
        case True:
            form = changePasswordForm(request.form)
            if request.method == "POST":
                oldPassword = request.form["oldPassword"]
                password = request.form["password"]
                passwordConfirm = request.form["passwordConfirm"]
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'select password from users where userName = "{session["userName"]}"'
                )
                if sha256_crypt.verify(oldPassword, cursor.fetchone()[0]):
                    if oldPassword == password:
                        flash("new password cant be same with old password", "error")
                        message("1", "NEW PASSWORD CANT BE SAME WITH OLD PASSWORD")
                    elif password != passwordConfirm:
                        message("1", "PASSWORDS MUST MATCH")
                        flash("passwords must match", "error")
                    elif oldPassword != password and password == passwordConfirm:
                        newPassword = sha256_crypt.hash(password)
                        connection = sqlite3.connect("db/users.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f'update users set password = "{newPassword}" where userName = "{session["userName"]}"'
                        )
                        connection.commit()
                        message("2", f'"{session["userName"]}" CHANGED HIS PASSWORD')
                        session.clear()
                        flash("you need login with new password", "error")
                        return redirect("/login")
                else:
                    flash("old password wrong", "error")
                    message("1", "OLD PASSWORD WRONG")

            return render_template(
                "changePassword.html",
                form=form,
                profilePicture=getProfilePicture(session["userName"]),
            )
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need login for change your password", "error")
            return redirect("/login")


@app.route("/post/<int:postID>", methods=["GET", "POST"])
def post(postID):
    form = commentForm(request.form)
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute(f"select id from posts")
    posts = str(cursor.fetchall())
    match str(postID) in posts:
        case True:
            message("2", f'"{postID}" FOUND')
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f'select * from posts where id = "{postID}"')
            post = cursor.fetchone()
            # cursor.execute(f'update posts set views = views+1 where id = "{postID}"')
            connection.commit()
            if request.method == "POST":
                comment = request.form["comment"]
                connection = sqlite3.connect("db/comments.db")
                cursor = connection.cursor()
                cursor.execute(
                    f"""
                    insert into comments(post,comment,user,date,time)
                    values({postID},"{comment}","{session["userName"]}",
                    "{currentDate()}",
                    "{currentTime()}")
                    """
                )
                connection.commit()
                return redirect(f"/post/{postID}")
            connection = sqlite3.connect("db/comments.db")
            cursor = connection.cursor()
            cursor.execute(f'select * from comments where post = "{postID}"')
            comments = cursor.fetchall()
            return render_template(
                "post.html",
                title=post[1],
                tags=post[2],
                content=post[3],
                author=post[4],
                views=post[5],
                date=post[5],
                form=form,
                comments=comments,
            )
        case False:
            message("1", "404")
            return render_template("404.html")


@app.route("/editpost/<int:postID>", methods=["GET", "POST"])
def editPost(postID):
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f"select id from posts")
            posts = str(cursor.fetchall())
            match str(postID) in posts:
                case True:
                    connection = sqlite3.connect("db/posts.db")
                    cursor = connection.cursor()
                    cursor.execute(f"select * from posts where id = {postID}")
                    post = cursor.fetchone()
                    message("2", f'"{postID}" FOUNDED')
                    connection = sqlite3.connect("db/users.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f'select userName from users where userName="{session["userName"]}"'
                    )
                    match post[4] == session["userName"]:
                        case True:
                            form = createPostForm(request.form)
                            form.postTitle.data = post[1]
                            form.postTags.data = post[2]
                            form.postContent.data = post[3]
                            if request.method == "POST":
                                postTitle = request.form["postTitle"]
                                postTags = request.form["postTags"]
                                postContent = request.form["postContent"]
                                connection = sqlite3.connect("db/posts.db")
                                cursor = connection.cursor()
                                cursor.execute(
                                    f'update posts set title = "{postTitle}" where id = {post[0]}'
                                )
                                cursor.execute(
                                    f'update posts set tags = "{postTags}" where id = {post[0]}'
                                )
                                cursor.execute(
                                    f'update posts set content = "{postContent}" where id = {post[0]}'
                                )
                                cursor.execute(
                                    f'update posts set lastEditDate = "{currentDate()}" where id = {post[0]}'
                                )
                                cursor.execute(
                                    f'update posts set lastEditTime = "{currentTime()}" where id = {post[0]}'
                                )
                                connection.commit()
                                message("2", f'"{postTitle}" EDITED')
                                return redirect("/")

                            return render_template(
                                "/editPost.html",
                                title=post[1],
                                tags=post[2],
                                content=post[3],
                                form=form,
                            )
                        case False:
                            flash("this post not yours", "error")
                            message(
                                "1",
                                f'THIS POST DOES NOT BELONG TO "{session["userName"]}"',
                            )
                            return redirect("/")
                case False:
                    message("1", f'"{postID}" NOT FOUND')
                    return render_template("404.html")
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need login for edit a post", "error")
            return redirect("/login")


@app.route("/dashboard/<userName>")
def dashboard(userName):
    match "userName" in session:
        case True:
            match session["userName"].lower() == userName:
                case True:
                    connection = sqlite3.connect("db/posts.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f'select * from posts where author = "{session["userName"]}"'
                    )
                    posts = cursor.fetchall()
                    return render_template(
                        "/dashboard.html",
                        posts=posts,
                    )
                case False:
                    message(
                        "1",
                        f'THIS IS DASHBOARD NOT BELONGS TO "{session["userName"]}"',
                    )
                    return redirect(f'/dashboard/{session["userName"].lower()}')
        case False:
            message("1", "USER NOT LOGGED IN (DASHBOARD)")
            flash("you need login for reach to dashboard", "error")
            return redirect("/login")


@app.route("/user/<int:userID>")
def user(userID):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(f"select userID from users")
    users = cursor.fetchall()
    match str(userID) in str(users):
        case True:
            message("2", f'USER "{userID}" FOUND')
            cursor.execute(f"select * from users where userID = {userID}")
            user = cursor.fetchone()
            print(user)
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f'select views from posts where author = "{user[1]}"')
            viewsData = cursor.fetchall()
            views = 0
            for view in viewsData:
                views += int(view[0])
            cursor.execute(f'select * from posts where author = "{user[1]}"')
            posts = cursor.fetchall()
            print(posts)
            message("2", f'USER "{userID}"s PAGE LOADED')
            return render_template(
                "user.html",
                user=user,
                views=views,
                posts=posts,
            )

        case _:
            message("1", f'USER "{userID}" NOT FOUND')
            return render_template("404.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static/images"),
        "favicon.png",
        mimetype="favicon.png",
    )


match __name__:
    case "__main__":
        app.run(debug=True)
