# Import the necessary modules and functions
import sqlite3
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from requests import post as requestsPost
from passlib.hash import sha512_crypt as encryption
from constants import (
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_PASSWORD_CHANGE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.log import Log
from utils.forms.ChangePasswordForm import ChangePasswordForm
from utils.flashMessage import flashMessage
from utils.addPoints import addPoints

# Create a blueprint for the change password route
changePasswordBlueprint = Blueprint("changePassword", __name__)


# Define the route for changing password
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
    # Check if user is logged in
    match "userName" in session:
        case True:
            # Initialize the change password form
            form = ChangePasswordForm(request.form)
            # Check if request method is POST
            match request.method == "POST":
                case True:
                    # Retrieve form data
                    oldPassword = request.form["oldPassword"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]
                    Log.database(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the database
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.database
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    # Retrieve hashed password from database
                    cursor.execute(
                        """select password from users where userName = ? """,
                        [(session["userName"])],
                    )
                    # Verify old password
                    match encryption.verify(oldPassword, cursor.fetchone()[0]):
                        case True:
                            # Check if new password is same as old password
                            match oldPassword == password:
                                case True:
                                    flashMessage(
                                        page="changePassword",
                                        message="same",
                                        category="error",
                                        language=session["language"],
                                    )  # Display a flash message
                            # Check if passwords match
                            match password != passwordConfirm:
                                case True:
                                    flashMessage(
                                        page="changePassword",
                                        message="match",
                                        category="error",
                                        language=session["language"],
                                    )  # Display a flash message
                            # Check if old password is different from new password and passwords match
                            match (
                                oldPassword != password and password == passwordConfirm
                            ):
                                case True:
                                    # Hash the new password
                                    newPassword = encryption.hash(password)
                                    Log.database(
                                        f"Connecting to '{DB_USERS_ROOT}' database"
                                    )  # Log the database connection is started
                                    # Connect to the database
                                    connection = sqlite3.connect(DB_USERS_ROOT)
                                    connection.set_trace_callback(
                                        Log.database
                                    )  # Set the trace callback for the connection
                                    # Check if RECAPTCHA is enabled for password change
                                    match RECAPTCHA and RECAPTCHA_PASSWORD_CHANGE:
                                        case True:
                                            # Get the reCAPTCHA response
                                            secretResponse = request.form[
                                                "g-recaptcha-response"
                                            ]
                                            # Verify the reCAPTCHA response
                                            verifyResponse = requestsPost(
                                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                            ).json()
                                            # Check if reCAPTCHA verification is successful
                                            match (
                                                verifyResponse["success"] is True
                                                or verifyResponse["score"] > 0.5
                                            ):
                                                case True:
                                                    # Log reCAPTCHA verification
                                                    Log.success(
                                                        f"Password change reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                    )
                                                    # Update password in the database
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update users set password = ? where userName = ? """,
                                                        [
                                                            (newPassword),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    # Commit the transaction
                                                    connection.commit()
                                                    # Log password change
                                                    Log.success(
                                                        f'User: "{session["userName"]}" changed his password',
                                                    )
                                                    # Clear session
                                                    session.clear()
                                                    flashMessage(
                                                        page="changePassword",
                                                        message="success",
                                                        category="success",
                                                        language=session["language"],
                                                    )  # Display a flash message
                                                    # Redirect to login page
                                                    return redirect("/login/redirect=&")
                                                case False:
                                                    # Log reCAPTCHA failure
                                                    Log.error(
                                                        f"Password change reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                    )
                                                    # Abort the request
                                                    abort(401)
                                        case False:
                                            # Update password in the database
                                            cursor = connection.cursor()
                                            cursor.execute(
                                                """update users set password = ? where userName = ? """,
                                                [
                                                    (newPassword),
                                                    (session["userName"]),
                                                ],
                                            )
                                            # Commit the transaction
                                            connection.commit()
                                            # Log password change
                                            Log.success(
                                                f'User: "{session["userName"]}" changed his password',
                                            )
                                            # Clear session
                                            session.clear()
                                            flashMessage(
                                                page="changePassword",
                                                message="success",
                                                category="success",
                                                language=session["language"],
                                            )  # Display a flash message
                                            # Redirect to login page
                                            return redirect("/login/redirect=&")
                        case _:
                            flashMessage(
                                page="changePassword",
                                message="old",
                                category="error",
                                language=session["language"],
                            )  # Display a flash message
            # Render the change password form template
            return render_template(
                "changePassword.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            # Log user not logged in
            Log.error(
                f"{request.remote_addr} tried to change his password without logging in"
            )
            flashMessage(
                page="changePassword",
                message="login",
                category="error",
                language=session["language"],
            )  # Display a flash message
            # Redirect to login page
            return redirect("/login/redirect=changepassword")
