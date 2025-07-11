from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import Settings
from utils.log import Log
from utils.paginate import paginate_query

adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments", methods=["GET", "POST"])
@adminPanelCommentsBlueprint.route("/adminpanel/comments", methods=["GET", "POST"])
def adminPanelComments():
    if "userName" in session:
        Log.info(f"Admin: {session['userName']} reached to comments admin panel")
        Log.database(f"Connecting to '{Settings.DB_COMMENTS_ROOT}' database")

        comments, page, total_pages = paginate_query(
            Settings.DB_COMMENTS_ROOT,
            "select count(*) from comments",
            "select * from comments order by timeStamp desc",
        )

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
