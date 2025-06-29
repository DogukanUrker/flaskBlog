import sqlite3

from flask import Blueprint, redirect, render_template, request, session
from settings import (
    DB_USERS_ROOT,
)
from utils.delete import Delete
from utils.log import Log

accountSettingsBlueprint = Blueprint("accountSettings", __name__)


@accountSettingsBlueprint.route("/accountsettings", methods=["GET", "POST"])
def accountSettings():
    if "userName" in session:
        Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

        connection = sqlite3.connect(DB_USERS_ROOT)
        connection.set_trace_callback(Log.database)
        cursor = connection.cursor()
        cursor.execute(
            """select userName from users where userName = ? """,
            [(session["userName"])],
        )
        user = cursor.fetchall()

        if request.method == "POST":
            Delete.user(user[0][0])
            return redirect("/")

        return render_template(
            "accountSettings.html",
            user=user,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to reach account settings without being logged in"
        )

        return redirect("/login/redirect=&accountsettings")
