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

adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments", methods=["GET", "POST"])
@adminPanelCommentsBlueprint.route("/adminpanel/comments", methods=["GET", "POST"])
def adminPanelComments():
    if "userName" in session:
        Log.info(f"Admin: {session['userName']} reached to comments admin panel")
        Log.database(f"Connecting to '{Settings.DB_COMMENTS_ROOT}' database")

        page = request.args.get("page", 1, type=int)
        per_page = 9

        connection = sqlite3.connect(Settings.DB_COMMENTS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute("select count(*) from comments")
        total_comments = cursor.fetchone()[0]
        total_pages = max(ceil(total_comments / per_page), 1)
        offset = (page - 1) * per_page
        cursor.execute(
            "select * from comments order by timeStamp desc limit ? offset ?",
            (per_page, offset),
        )
        comments = cursor.fetchall()

        Log.info(f"Rendering adminPanelComments.html: params: comments={comments}")

        return render_template(
            "adminPanelComments.html",
            comments=comments,
            page=page,
            total_pages=total_pages,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to reach comment admin panel being logged in"
        )

        return redirect("/")
