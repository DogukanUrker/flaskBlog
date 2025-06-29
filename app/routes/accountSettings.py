import sqlite3

from flask import Blueprint, abort, redirect, render_template, request, session
from requests import post as requestsPost
from settings import (
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_DELETE_USER,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
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
            if RECAPTCHA and RECAPTCHA_DELETE_USER:
                secretResponse = request.form["g-recaptcha-response"]

                verifyResponse = requestsPost(
                    url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                ).json()

                if verifyResponse["success"] is True or verifyResponse["score"] > 0.5:
                    Log.success(
                        f"User delete reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                    )

                    Delete.user(user[0][0])

                    return redirect("/")
                else:
                    Log.error(
                        f"User delete reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                    )

                    abort(401)
            else:
                Delete.user(user[0][0])

                return redirect("/")

        return render_template(
            "accountSettings.html.jinja",
            user=user,
            siteKey=RECAPTCHA_SITE_KEY,
            recaptcha=RECAPTCHA,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to reach account settings without being logged in"
        )

        return redirect("/login/redirect=&accountsettings")
