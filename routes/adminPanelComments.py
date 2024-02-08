from helpers import (
    sqlite3,
    render_template,
    Blueprint,
    session,
    redirect,
    request,
)
from delete import deleteComment

adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments", methods=["GET", "POST"])
@adminPanelCommentsBlueprint.route("/adminpanel/comments", methods=["GET", "POST"])
def adminPanelComments():
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            role = cursor.fetchone()[0]
            if request.method == "POST":
                if "commentDeleteButton" in request.form:
                    deleteComment(request.form["commentID"])
                    return redirect(f"/admin/comments")
            match role == "admin":
                case True:
                    connection = sqlite3.connect("db/comments.db")
                    cursor = connection.cursor()
                    cursor.execute("select * from comments")
                    comments = cursor.fetchall()
                    return render_template("adminPanelComments.html", comments=comments)
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
