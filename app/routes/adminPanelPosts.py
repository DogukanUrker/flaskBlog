import sqlite3
from math import ceil

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import Settings
from utils.log import Log

adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts", methods=["GET", "POST"])
@adminPanelPostsBlueprint.route("/adminpanel/posts", methods=["GET", "POST"])
def adminPanelPosts():
    if "userName" in session:
        Log.info(f"Admin: {session['userName']} reached to posts admin panel")
        Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

        page = request.args.get("page", 1, type=int)
        per_page = 9

        connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute("select count(*) from posts")
        total_posts = cursor.fetchone()[0]
        total_pages = max(ceil(total_posts / per_page), 1)
        offset = (page - 1) * per_page
        cursor.execute(
            "select * from posts order by timeStamp desc limit ? offset ?",
            (per_page, offset),
        )
        posts = cursor.fetchall()

        Log.info(
            f"Rendering dashboard.html: params: posts={len(posts)} and showPosts=True"
        )

        return render_template(
            "dashboard.html",
            posts=posts,
            showPosts=True,
            page=page,
            total_pages=total_pages,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to reach post admin panel being logged in"
        )

        return redirect("/")
