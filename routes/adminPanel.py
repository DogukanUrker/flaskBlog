from helpers import (
    sqlite3,
    session,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    render_template,
)

adminPanelBlueprint = Blueprint("adminPanel", __name__)


@adminPanelBlueprint.route("/admin")
def adminPanel():
    match "userName" in session:
        case True:
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select role from users where userName = ? """,
                [(session["userName"])],
            )
            role = cursor.fetchone()[0]
            match role == "admin":
                case True:
                    return render_template("adminPanel.html")
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
