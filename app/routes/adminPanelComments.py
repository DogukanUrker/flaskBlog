import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import (
    DB_COMMENTS_ROOT,
)
from utils.log import Log

adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments", methods=["GET", "POST"])
@adminPanelCommentsBlueprint.route("/adminpanel/comments", methods=["GET", "POST"])
def adminPanelComments():
    match "userName" in session:
        case True:
            Log.info(f"Admin: {session['userName']} reached to comments admin panel")
            Log.database(f"Connecting to '{DB_COMMENTS_ROOT}' database")

            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()
            cursor.execute("select * from comments order by timeStamp desc")
            comments = cursor.fetchall()

            Log.info(
                f"Rendering adminPanelComments.html.jinja: params: comments={comments}"
            )

            return render_template("adminPanelComments.html.jinja", comments=comments)
        case False:
            Log.error(
                f"{request.remote_addr} tried to reach comment admin panel being logged in"
            )

            return redirect("/")
