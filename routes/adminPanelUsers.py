from helpers import (
    sqlite3,
    session,
    request,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    changeUserRole,
    render_template,
)
from delete import deleteUser

adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


@adminPanelUsersBlueprint.route("/admin/users", methods=["GET", "POST"])
@adminPanelUsersBlueprint.route("/adminpanel/users", methods=["GET", "POST"])
def adminPanelUsers():
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
                    match "userDeleteButton" in request.form:
                        case True:
                            deleteUser(request.form["userName"])
                    match "userRoleChangeButton" in request.form:
                        case True:
                            changeUserRole(request.form["userName"])
            match role == "admin":
                case True:
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute("select * from users")
                    users = cursor.fetchall()
                    return render_template(
                        "adminPanelUsers.html",
                        users=users,
                    )
                case False:
                    return redirect("/")
        case False:
            return redirect("/")
