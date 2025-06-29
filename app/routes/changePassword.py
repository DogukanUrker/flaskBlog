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
    RECAPTCHA,
    RECAPTCHA_PASSWORD_CHANGE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.flashMessage import flashMessage
from utils.forms.ChangePasswordForm import ChangePasswordForm
from utils.log import Log

changePasswordBlueprint = Blueprint("changePassword", __name__)


@changePasswordBlueprint.route("/changepassword", methods=["GET", "POST"])
def changePassword():
    """
    This function is the route for the change password page.
    It is used to change the user's password.

    Args:
        request.form (dict): the form data from the request

    Returns:
        render_template: a rendered template with the form and reCAPTCHA

    Raises:
        401: if the reCAPTCHA is not passed
    """

    match "userName" in session:
        case True:
            form = ChangePasswordForm(request.form)

            match request.method == "POST":
                case True:
                    oldPassword = request.form["oldPassword"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]
                    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(Log.database)
                    cursor = connection.cursor()

                    cursor.execute(
                        """select password from users where userName = ? """,
                        [(session["userName"])],
                    )

                    match encryption.verify(oldPassword, cursor.fetchone()[0]):
                        case True:
                            match oldPassword == password:
                                case True:
                                    flashMessage(
                                        page="changePassword",
                                        message="same",
                                        category="error",
                                        language=session["language"],
                                    )

                            match password != passwordConfirm:
                                case True:
                                    flashMessage(
                                        page="changePassword",
                                        message="match",
                                        category="error",
                                        language=session["language"],
                                    )

                            match (
                                oldPassword != password and password == passwordConfirm
                            ):
                                case True:
                                    newPassword = encryption.hash(password)
                                    Log.database(
                                        f"Connecting to '{DB_USERS_ROOT}' database"
                                    )

                                    connection = sqlite3.connect(DB_USERS_ROOT)
                                    connection.set_trace_callback(Log.database)

                                    match RECAPTCHA and RECAPTCHA_PASSWORD_CHANGE:
                                        case True:
                                            secretResponse = request.form[
                                                "g-recaptcha-response"
                                            ]

                                            verifyResponse = requestsPost(
                                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                            ).json()

                                            match (
                                                verifyResponse["success"] is True
                                                or verifyResponse["score"] > 0.5
                                            ):
                                                case True:
                                                    Log.success(
                                                        f"Password change reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                    )

                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update users set password = ? where userName = ? """,
                                                        [
                                                            (newPassword),
                                                            (session["userName"]),
                                                        ],
                                                    )

                                                    connection.commit()

                                                    Log.success(
                                                        f'User: "{session["userName"]}" changed his password',
                                                    )

                                                    session.clear()
                                                    flashMessage(
                                                        page="changePassword",
                                                        message="success",
                                                        category="success",
                                                        language=session["language"],
                                                    )

                                                    return redirect("/login/redirect=&")
                                                case False:
                                                    Log.error(
                                                        f"Password change reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                    )

                                                    abort(401)
                                        case False:
                                            cursor = connection.cursor()
                                            cursor.execute(
                                                """update users set password = ? where userName = ? """,
                                                [
                                                    (newPassword),
                                                    (session["userName"]),
                                                ],
                                            )

                                            connection.commit()

                                            Log.success(
                                                f'User: "{session["userName"]}" changed his password',
                                            )

                                            session.clear()
                                            flashMessage(
                                                page="changePassword",
                                                message="success",
                                                category="success",
                                                language=session["language"],
                                            )

                                            return redirect("/login/redirect=&")
                        case _:
                            flashMessage(
                                page="changePassword",
                                message="old",
                                category="error",
                                language=session["language"],
                            )

            return render_template(
                "changePassword.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            Log.error(
                f"{request.remote_addr} tried to change his password without logging in"
            )
            flashMessage(
                page="changePassword",
                message="login",
                category="error",
                language=session["language"],
            )

            return redirect("/login/redirect=changepassword")
