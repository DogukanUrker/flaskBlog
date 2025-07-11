import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import Settings
from utils.changeUserRole import changeUserRole
from utils.delete import Delete
from utils.log import Log
from utils.paginate import paginate_query

adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


@adminPanelUsersBlueprint.route("/admin/users", methods=["GET", "POST"])
@adminPanelUsersBlueprint.route("/adminpanel/users", methods=["GET", "POST"])
def adminPanelUsers():
    if "userName" in session:
        Log.info(f"Admin: {session['userName']} reached to users admin panel")
        Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

        connection = sqlite3.connect(Settings.DB_USERS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute(
            """select role from users where userName = ? """,
            [(session["userName"])],
        )
        role = cursor.fetchone()[0]

        if request.method == "POST":
            if "userDeleteButton" in request.form:
                Log.info(
                    f"Admin: {session['userName']} deleted user: {request.form['userName']}"
                )

                Delete.user(request.form["userName"])

            if "userRoleChangeButton" in request.form:
                Log.info(
                    f"Admin: {session['userName']} changed {request.form['userName']}'s role"
                )

                changeUserRole(request.form["userName"])

        if role == "admin":
            users, page, total_pages = paginate_query(
                Settings.DB_USERS_ROOT,
                "select count(*) from users",
                "select * from users",
            )

            Log.info(f"Rendering adminPanelUsers.html: params: users={users}")

            return render_template(
                "adminPanelUsers.html",
                users=users,
                page=page,
                total_pages=total_pages,
            )
        else:
            Log.error(
                f"{request.remote_addr} tried to reach user admin panel without being admin"
            )

            return redirect("/")
    else:
        Log.error(
            f"{request.remote_addr} tried to reach user admin panel being logged in"
        )

        return redirect("/")
