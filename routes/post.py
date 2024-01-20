from helpers import (
    flash,
    session,
    sqlite3,
    request,
    message,
    url_for,
    APP_NAME,
    redirect,
    addPoints,
    Blueprint,
    currentDate,
    currentTime,
    commentForm,
    DB_POSTS_ROOT,
    DB_COMMENTS_ROOT,
    render_template,
)
from delete import deleteComment, deletePost

postBlueprint = Blueprint("post", __name__)


@postBlueprint.route("/post/<int:postID>", methods=["GET", "POST"])
def post(postID):
    form = commentForm(request.form)
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    cursor.execute("select id from posts")
    posts = str(cursor.fetchall())
    match str(postID) in posts:
        case True:
            message("2", f'POST: "{postID}" FOUND')
            connection = sqlite3.connect(DB_POSTS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select * from posts where id = ? """,
                [(postID)],
            )
            post = cursor.fetchone()
            cursor.execute(
                """update posts set views = views+1 where id = ? """,
                [(postID)],
            )
            connection.commit()
            match request.method == "POST":
                case True:
                    match "postDeleteButton" in request.form:
                        case True:
                            deletePost(postID)
                            return redirect(f"/")
                    match "commentDeleteButton" in request.form:
                        case True:
                            deleteComment(request.form["commentID"])
                            return redirect(url_for("post.post", postID=postID)), 301
                    comment = request.form["comment"]
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        "insert into comments(post,comment,user,date,time) \
                        values(?, ?, ?, ?, ?)",
                        (
                            postID,
                            comment,
                            session["userName"],
                            currentDate(),
                            currentTime(),
                        ),
                    )
                    connection.commit()
                    message(
                        "2",
                        f'USER: "{session["userName"]}" COMMENTED TO POST: "{postID}"',
                    )
                    addPoints(5, session["userName"])
                    flash("You earned 5 points by commenting ", "success")
                    return redirect(url_for("post.post", postID=postID)), 301
            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select * from comments where post = ? """,
                [(postID)],
            )
            comments = cursor.fetchall()
            return render_template(
                "post.html",
                id=post[0],
                title=post[1],
                tags=post[2],
                content=post[3],
                author=post[4],
                views=post[7],
                date=post[5],
                time=post[6],
                form=form,
                comments=comments,
                appName=APP_NAME,
            )
        case False:
            return render_template("404.html")
