import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import (
    DB_POSTS_ROOT,
)
from utils.log import Log

adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts", methods=["GET", "POST"])
@adminPanelPostsBlueprint.route("/adminpanel/posts", methods=["GET", "POST"])
def adminPanelPosts():
    if "userName" in session:
        Log.info(f"Admin: {session['userName']} reached to posts admin panel")
        Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

        connection = sqlite3.connect(DB_POSTS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute("select * from posts order by timeStamp desc")
        posts = cursor.fetchall()

        Log.info(
            f"Rendering dashboard.html.jinja: params: posts={len(posts)} and showPosts=True"
        )

        return render_template("dashboard.html.jinja", posts=posts, showPosts=True)
    else:
        Log.error(
            f"{request.remote_addr} tried to reach post admin panel being logged in"
        )

        return redirect("/")
