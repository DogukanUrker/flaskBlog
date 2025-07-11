import sqlite3

from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    session,
)
from passlib.hash import sha512_crypt as encryption
from requests import post as requestsPost
from settings import Settings
from utils.addPoints import add_points
from utils.flashMessage import flash_message
from utils.forms.LoginForm import LoginForm
from utils.log import Log

login_blueprint = Blueprint("login", __name__)


@login_blueprint.route("/login/redirect=<direct>", methods=["GET", "POST"])
def login(direct):
    """
    This function handles the login process for the website.

    Args:
        direct (str): The direct link to redirect to after login.

    Returns:
        tuple: A tuple containing the redirect response and status code.

    Raises:
        401: If the login is unsuccessful.
    """
    direct = direct.replace("&", "/")
    if Settings.LOG_IN:
        if "user_name" in session:
            Log.error(f'User: "{session["user_name"]}" already logged in')
            return (
                redirect(direct),
                301,
            )
        else:
            form = LoginForm(request.form)
            if request.method == "POST":
                user_name = request.form["user_name"]
                password = request.form["password"]
                user_name = user_name.replace(" ", "")
                Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")
                connection = sqlite3.connect(Settings.DB_USERS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()
                cursor.execute(
                    """select * from users where lower(user_name) = ? """,
                    [(user_name.lower())],
                )
                user = cursor.fetchone()
                if not user:
                    Log.error(f'User: "{user_name}" not found')
                    flash_message(
                        page="login",
                        message="notFound",
                        category="error",
                        language=session["language"],
                    )
                else:
                    if encryption.verify(password, user[3]):
                        if Settings.RECAPTCHA:
                            secretResponse = request.form["g-recaptcha-response"]
                            verifyResponse = requestsPost(
                                url=f"{Settings.RECAPTCHA_VERIFY_URL}?secret={Settings.RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                            ).json()
                            if not (
                                verifyResponse["success"] is True
                                or verifyResponse.get("score", 0) > 0.5
                            ):
                                Log.error(
                                    f"Login reCAPTCHA | verification: {verifyResponse.get('success')} | score: {verifyResponse.get('score')}",
                                )
                                abort(401)

                            Log.success(
                                f"Login reCAPTCHA | verification: {verifyResponse['success']} | score: {verifyResponse.get('score')}",
                            )

                        session["user_name"] = user[1]
                        session["user_role"] = user[5]
                        add_points(1, session["user_name"])
                        Log.success(f'User: "{user[1]}" logged in')
                        flash_message(
                            page="login",
                            message="success",
                            category="success",
                            language=session["language"],
                        )

                        return (
                            redirect(direct),
                            301,
                        )

                    else:
                        Log.error("Wrong password")
                        flash_message(
                            page="login",
                            message="password",
                            category="error",
                            language=session["language"],
                        )

            return render_template(
                "login.html",
                form=form,
                hideLogin=True,
                siteKey=Settings.RECAPTCHA_SITE_KEY,
                recaptcha=Settings.RECAPTCHA,
            )
    else:
        return (
            redirect(direct),
            301,
        )
