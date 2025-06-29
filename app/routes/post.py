import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from settings import (
    ANALYTICS,
    APP_NAME,
    DB_ANALYTICS_ROOT,
    DB_COMMENTS_ROOT,
    DB_POSTS_ROOT,
)
from utils.addPoints import addPoints
from utils.calculateReadTime import calculateReadTime
from utils.delete import Delete
from utils.flashMessage import flashMessage
from utils.forms.CommentForm import CommentForm
from utils.generateUrlIdFromPost import getSlugFromPostTitle
from utils.getDataFromUserIP import getDataFromUserIP
from utils.log import Log
from utils.time import currentTimeStamp

postBlueprint = Blueprint("post", __name__)


@postBlueprint.route("/post/<urlID>", methods=["GET", "POST"])
@postBlueprint.route("/post/<slug>-<urlID>", methods=["GET", "POST"])
def post(urlID=None, slug=None):
    form = CommentForm(request.form)

    Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

    connection = sqlite3.connect(DB_POSTS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()

    cursor.execute("select urlID, title from posts where urlID = ?", (urlID,))
    posts = cursor.fetchone()

    match str(urlID) in posts:
        case True:
            postSlug = getSlugFromPostTitle(posts[1])

            match slug == postSlug:
                case True:
                    pass

                case False:
                    return redirect(url_for("post.post", urlID=urlID, slug=postSlug))

            Log.success(f'post: "{urlID}" loaded')

            Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

            connection = sqlite3.connect(DB_POSTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                """select * from posts where urlID = ? """,
                [(urlID)],
            )
            post = cursor.fetchone()

            cursor.execute(
                """update posts set views = views+1 where id = ? """,
                [(post[0])],
            )
            connection.commit()

            match request.method == "POST":
                case True:
                    match "postDeleteButton" in request.form:
                        case True:
                            Delete.post(post[0])

                            return redirect("/")

                    match "commentDeleteButton" in request.form:
                        case True:
                            Delete.comment(request.form["commentID"])

                            return redirect(url_for("post.post", urlID=urlID)), 301

                    comment = request.form["comment"]

                    Log.database(f"Connecting to '{DB_COMMENTS_ROOT}' database")

                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    connection.set_trace_callback(Log.database)
                    cursor = connection.cursor()

                    cursor.execute(
                        "insert into comments(post,comment,user,timeStamp) \
                        values(?, ?, ?, ?)",
                        (
                            post[0],
                            comment,
                            session["userName"],
                            currentTimeStamp(),
                        ),
                    )
                    connection.commit()

                    Log.success(
                        f'User: "{session["userName"]}" commented to post: "{urlID}"',
                    )

                    addPoints(5, session["userName"])

                    flashMessage(
                        page="post",
                        message="success",
                        category="success",
                        language=session["language"],
                    )

                    return redirect(url_for("post.post", urlID=urlID)), 301

            Log.database(f"Connecting to '{DB_COMMENTS_ROOT}' database")

            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                """select * from comments where post = ? order by timeStamp desc""",
                [(post[0])],
            )
            comments = cursor.fetchall()

            match ANALYTICS:
                case True:
                    userIPData = getDataFromUserIP(
                        str(request.headers.get("User-Agent"))
                    )
                    idForRandomVisitor = None
                    match "userName" in session:
                        case True:
                            sessionUser = session["userName"]
                        case False:
                            sessionUser = "unsignedUser"
                    match userIPData["status"] == 0:
                        case True:
                            Log.database(
                                f"Connecting to '{DB_ANALYTICS_ROOT}' database"
                            )

                            connection = sqlite3.connect(DB_ANALYTICS_ROOT)
                            connection.set_trace_callback(Log.database)
                            cursor = connection.cursor()

                            cursor.execute(
                                """insert into postsAnalytics (postID, visitorUserName, country, os, continent, timeStamp) values (?,?,?,?,?,?) RETURNING id""",
                                (
                                    post[0],
                                    sessionUser,
                                    userIPData["payload"]["country"],
                                    userIPData["payload"]["os"],
                                    userIPData["payload"]["continent"],
                                    currentTimeStamp(),
                                ),
                            )
                            idForRandomVisitor = cursor.fetchone()[0]
                            connection.commit()
                            connection.close()
                        case False:
                            Log.error(
                                f"Aborting postsAnalytics, {userIPData['message']}"
                            )

                case False:
                    pass

            return render_template(
                "post.html.jinja",
                id=post[0],
                title=post[1],
                tags=post[2],
                content=post[3],
                author=post[5],
                views=post[6],
                timeStamp=post[7],
                lastEditTimeStamp=post[8],
                urlID=post[10],
                form=form,
                comments=comments,
                appName=APP_NAME,
                blogPostUrl=request.root_url,
                readingTime=calculateReadTime(post[3]),
                idForRandomVisitor=idForRandomVisitor,
            )

        case False:
            Log.error(f"{request.remote_addr} tried to reach unknown post")

            return render_template("notFound.html.jinja")
