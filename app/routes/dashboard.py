import sqlite3
from json import load
from math import ceil

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from settings import Settings
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
            Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

            page = request.args.get("page", 1, type=int)
            per_page = 9

            connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                "select count(*) from posts where author = ?",
                [(session["userName"])],
            )
            total_posts = cursor.fetchone()[0]
            total_pages = max(ceil(total_posts / per_page), 1)

            offset = (page - 1) * per_page
            cursor.execute(
                """select * from posts where author = ? order by timeStamp desc limit ? offset ?""",
                (session["userName"], per_page, offset),
            )
            posts = cursor.fetchall()
            Log.database(f"Connecting to '{Settings.DB_COMMENTS_ROOT}' database")

            connection = sqlite3.connect(Settings.DB_COMMENTS_ROOT)
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
                page=page,
                total_pages=total_pages,
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
