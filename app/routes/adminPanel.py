import sqlite3

from flask import Blueprint, redirect, render_template, request, session
from settings import DB_USERS_ROOT
from utils.log import Log

adminPanelBlueprint = Blueprint("adminPanel", __name__)


@adminPanelBlueprint.route("/admin")
def adminPanel():
    if "userName" in session:
        Log.success(f"Connecting to '{DB_USERS_ROOT}' database")

        connection = sqlite3.connect(DB_USERS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute(
            """select role from users where userName = ? """,
            [(session["userName"])],
        )
        role = cursor.fetchone()[0]

        if role == "admin":
            Log.info(f"Admin: {session['userName']} reached to the admin panel")

            Log.info("Rendering adminPanel.html.jinja: params: None")

            return render_template("adminPanel.html.jinja")
        else:
            Log.error(
                f"{request.remote_addr} tried to reach admin panel without being admin"
            )

            return redirect("/")
    else:
        Log.error(f"{request.remote_addr} tried to reach admin panel being logged in")

        return redirect("/")
