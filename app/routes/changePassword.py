import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from passlib.hash import sha512_crypt as encryption
from settings import Settings
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
        render_template: a rendered template with the form
    """

    if "userName" in session:
        form = ChangePasswordForm(request.form)

        if request.method == "POST":
            oldPassword = request.form["oldPassword"]
            password = request.form["password"]
            passwordConfirm = request.form["passwordConfirm"]
            Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

            connection = sqlite3.connect(Settings.DB_USERS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                """select password from users where userName = ? """,
                [(session["userName"])],
            )

            if encryption.verify(oldPassword, cursor.fetchone()[0]):
                if oldPassword == password:
                    flashMessage(
                        page="changePassword",
                        message="same",
                        category="error",
                        language=session["language"],
                    )

                if password != passwordConfirm:
                    flashMessage(
                        page="changePassword",
                        message="match",
                        category="error",
                        language=session["language"],
                    )

                if oldPassword != password and password == passwordConfirm:
                    newPassword = encryption.hash(password)
                    Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

                    connection = sqlite3.connect(Settings.DB_USERS_ROOT)
                    connection.set_trace_callback(Log.database)
                    cursor = connection.cursor()
                    cursor.execute(
                        """update users set password = ? where userName = ? """,
                        [(newPassword), (session["userName"])],
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
            else:
                flashMessage(
                    page="changePassword",
                    message="old",
                    category="error",
                    language=session["language"],
                )

        return render_template(
            "changePassword.html",
            form=form,
        )
    else:
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
