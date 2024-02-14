# Import the necessary modules and functions
from modules import (
    Log,  # Importing log class for logging messages
    flash,  # Importing flash function for displaying messages
    abort,  # Importing abort function for aborting requests
    session,  # Importing session for managing user sessions
    sqlite3,  # Importing sqlite3 for working with SQLite databases
    request,  # Importing request for handling HTTP requests
    redirect,  # Importing redirect for redirecting requests
    Blueprint,  # Importing Blueprint for creating modular applications
    RECAPTCHA,  # Importing RECAPTCHA constant
    encryption,  # Importing encryption functions for password hashing and verification
    requestsPost,  # Importing requestsPost function for making HTTP POST requests
    DB_USERS_ROOT,  # Importing constant for database path
    render_template,  # Importing render_template for rendering HTML templates
    ChangePasswordForm,  # Importing form class for change password form
    RECAPTCHA_SITE_KEY,  # Importing RECAPTCHA site key
    RECAPTCHA_VERIFY_URL,  # Importing RECAPTCHA verification URL
    RECAPTCHA_SECRET_KEY,  # Importing RECAPTCHA secret key
    RECAPTCHA_PASSWORD_CHANGE,  # Importing RECAPTCHA flag for password change verification
)

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
                    Log.sql(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the database
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
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
                                    # Display error message
                                    flash(
                                        "New password can not be same with old password.",
                                        "error",
                                    )
                            # Check if passwords match
                            match password != passwordConfirm:
                                case True:
                                    # Display error message
                                    flash("Passwords must match.", "error")
                            # Check if old password is different from new password and passwords match
                            match oldPassword != password and password == passwordConfirm:
                                case True:
                                    # Hash the new password
                                    newPassword = encryption.hash(password)
                                    Log.sql(
                                        f"Connecting to '{DB_USERS_ROOT}' database"
                                    )  # Log the database connection is started
                                    # Connect to the database
                                    connection = sqlite3.connect(DB_USERS_ROOT)
                                    connection.set_trace_callback(
                                        Log.sql
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
                                            match verifyResponse[
                                                "success"
                                            ] == True or verifyResponse["score"] > 0.5:
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
                                                    # Display success message
                                                    flash(
                                                        "You need login with new password.",
                                                        "success",
                                                    )
                                                    # Redirect to login page
                                                    return redirect("/login/redirect=&")
                                                case False:
                                                    # Log reCAPTCHA failure
                                                    Log.danger(
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
                                            # Display success message
                                            flash(
                                                "You need login with new password.",
                                                "success",
                                            )
                                            # Redirect to login page
                                            return redirect("/login/redirect=&")
                        case _:
                            # Display error message
                            flash("Old is password wrong.", "error")
            # Render the change password form template
            return render_template(
                "changePassword.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            # Log user not logged in
            Log.danger(
                f"{request.remote_addr} tried to change his password without logging in"
            )
            # Display error message
            flash("You need login for change your password.", "error")
            # Redirect to login page
            return redirect("/login/redirect=changepassword")
