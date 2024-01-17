from helpers import (
    request,
    sqlite3,
    session,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    render_template,
    DB_COMMENTS_ROOT,
)
from delete import deleteComment

adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments", methods=["GET", "POST"])
@adminPanelCommentsBlueprint.route("/adminpanel/comments", methods=["GET", "POST"])
def adminPanelComments():
    match "userName" in session:
        case True:
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select role from users where userName = ? """,
                [(session["userName"])],
            )
            role = cursor.fetchone()[0]
            match request.method == "POST":
                case True:
                    match "commentDeleteButton" in request.form:
                        case True:
                            deleteComment(request.form["commentID"])
                    return redirect(f"/admin/comments")
            match role == "admin":
                case True:
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute("select * from comments")
                    comments = cursor.fetchall()
                    return render_template("adminPanelComments.html", comments=comments)
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
