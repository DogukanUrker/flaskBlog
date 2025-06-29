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
from settings import (
    DB_USERS_ROOT,
    LOG_IN,
    RECAPTCHA,
    RECAPTCHA_LOGIN,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.addPoints import addPoints
from utils.flashMessage import flashMessage
from utils.forms.LoginForm import LoginForm
from utils.log import Log

loginBlueprint = Blueprint("login", __name__)


@loginBlueprint.route("/login/redirect=<direct>", methods=["GET", "POST"])
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
    if LOG_IN:
        if "userName" in session:
            Log.error(f'User: "{session["userName"]}" already logged in')
            return (
                redirect(direct),
                301,
            )
        else:
            form = LoginForm(request.form)
            if request.method == "POST":
                userName = request.form["userName"]
                password = request.form["password"]
                userName = userName.replace(" ", "")
                Log.database(f"Connecting to '{DB_USERS_ROOT}' database")
                connection = sqlite3.connect(DB_USERS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()
                cursor.execute(
                    """select * from users where lower(userName) = ? """,
                    [(userName.lower())],
                )
                user = cursor.fetchone()
                if not user:
                    Log.error(f'User: "{userName}" not found')
                    flashMessage(
                        page="login",
                        message="notFound",
                        category="error",
                        language=session["language"],
                    )
                else:
                    if encryption.verify(password, user[3]):
                        if RECAPTCHA and RECAPTCHA_LOGIN:
                            secretResponse = request.form["g-recaptcha-response"]
                            verifyResponse = requestsPost(
                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                            ).json()
                            if (
                                verifyResponse["success"] is True
                                or verifyResponse["score"] > 0.5
                            ):
                                Log.success(
                                    f"Login reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                )
                                session["userName"] = user[1]
                                session["userRole"] = user[5]
                                addPoints(1, session["userName"])
                                Log.success(
                                    f'User: "{user[1]}" logged in',
                                )
                                flashMessage(
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
                                Log.error(
                                    f"Login reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                )
                                abort(401)

                        else:
                            session["userName"] = user[1]
                            session["userRole"] = user[5]

                            addPoints(1, session["userName"])
                            Log.success(
                                f'User: "{user[1]}" logged in',
                            )
                            flashMessage(
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
                        flashMessage(
                            page="login",
                            message="password",
                            category="error",
                            language=session["language"],
                        )

            return render_template(
                "login.html.jinja",
                form=form,
                hideLogin=True,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
    else:
        return (
            redirect(direct),
            301,
        )
