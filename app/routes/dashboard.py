import sqlite3
from json import load

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from settings import DB_COMMENTS_ROOT, DB_POSTS_ROOT
from utils.delete import Delete
from utils.flashMessage import flashMessage
from utils.log import Log

dashboardBlueprint = Blueprint("dashboard", __name__)


@dashboardBlueprint.route("/dashboard/<userName>", methods=["GET", "POST"])
def dashboard(userName):
    if "userName" in session:
        if session["userName"].lower() == userName.lower():
            if request.method == "POST":
                if "postDeleteButton" in request.form:
                    Delete.post(request.form["postID"])

                    return (
                        redirect(url_for("dashboard.dashboard", userName=userName)),
                        301,
                    )
            Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

            connection = sqlite3.connect(DB_POSTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                """select * from posts where author = ? order by timeStamp desc""",
                [(session["userName"])],
            )
            posts = cursor.fetchall()
            Log.database(f"Connecting to '{DB_COMMENTS_ROOT}' database")

            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                """select * from comments where lower(user) = ? order by timeStamp desc""",
                [(userName.lower())],
            )
            comments = cursor.fetchall()

            if posts == []:
                showPosts = False
            else:
                showPosts = True

            if comments == []:
                showComments = False
            else:
                showComments = True

            posts = list(posts)

            for i in range(len(posts)):
                posts[i] = list(posts[i])

            language = session.get("language")
            translationFile = f"./translations/{language}.json"

            with open(translationFile, "r", encoding="utf-8") as file:
                translations = load(file)

            for post in posts:
                post[9] = translations["categories"][post[9].lower()]

            return render_template(
                "/dashboard.html",
                posts=posts,
                comments=comments,
                showPosts=showPosts,
                showComments=showComments,
            )
        else:
            Log.error(
                f'User: "{session["userName"]}" tried to login to another users dashboard',
            )

            return redirect(f"/dashboard/{session['userName'].lower()}")
    else:
        Log.error(f"{request.remote_addr} tried to access the dashboard without login")
        flashMessage(
            page="dashboard",
            message="login",
            category="error",
            language=session["language"],
        )

        return redirect("/login/redirect=&dashboard&user")
