# Import necessary modules and functions
import sqlite3
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from requests import post as requestsPost
from constants import (
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_USERNAME_CHANGE,
    RECAPTCHA_VERIFY_URL,
)
from utils.log import Log
from utils.forms.ChangeUserNameForm import ChangeUserNameForm
from utils.flashMessage import flashMessage
from utils.addPoints import addPoints

# Create a blueprint for the change username route
changeUserNameBlueprint = Blueprint("changeUserName", __name__)


# Define a route for changing username
@changeUserNameBlueprint.route("/changeusername", methods=["GET", "POST"])
def changeUserName():
    """
    Checks if the user is logged in:
    If the user is not logged in, they are redirected to the homepage.

    Checks if the user has submitted a new username:
    If the user has submitted a new username, the new username is checked to ensure it meets the requirements.

    If the new username meets the requirements:
    The user's details are updated in the database.
    The user is redirected to their profile page.

    If the new username does not meet the requirements:
    An error message is displayed.

    Returns:
    The change username template with the form and reCAPTCHA.
    """
    # Check if "userName" exists in session
    match "userName" in session:
        case True:
            # Create form instance
            form = ChangeUserNameForm(request.form)
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Retrieve new username from the form
                    newUserName = request.form["newUserName"]
                    newUserName = newUserName.replace(
                        " ", ""
                    )  # Remove spaces from username
                    Log.database(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the users database
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.database
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    cursor.execute(
                        """select userName from users where userName = ? """,
                        [(newUserName)],
                    )
                    userNameCheck = (
                        cursor.fetchone()
                    )  # Check if new username already exists
                    # Check if new username contains only ASCII characters
                    match newUserName.isascii():
                        case True:
                            # Check if new username is the same as the current username
                            match newUserName == session["userName"]:
                                case True:
                                    flashMessage(
                                        page="changeUserName",
                                        message="same",
                                        category="error",
                                        language=session["language"],
                                    )  # Display a flash message
                                case False:
                                    # Check if new username is available
                                    match userNameCheck is None:
                                        case True:
                                            # Check Recaptcha if enabled
                                            match (
                                                RECAPTCHA and RECAPTCHA_USERNAME_CHANGE
                                            ):
                                                case True:
                                                    # Verify Recaptcha response
                                                    secretResponse = request.form[
                                                        "g-recaptcha-response"
                                                    ]
                                                    verifyResponse = requestsPost(
                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                    ).json()
                                                    # Check Recaptcha verification result
                                                    match (
                                                        verifyResponse["success"]
                                                        is True
                                                        or verifyResponse["score"] > 0.5
                                                    ):
                                                        case True:
                                                            # Log the reCAPTCHA verification result
                                                            Log.success(
                                                                f"Change username reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            # Update username in the database
                                                            cursor.execute(
                                                                """update users set userName = ? where userName = ? """,
                                                                [
                                                                    (newUserName),
                                                                    (
                                                                        session[
                                                                            "userName"
                                                                        ]
                                                                    ),
                                                                ],
                                                            )
                                                            connection.commit()
                                                            # Update username in posts database
                                                            connection = (
                                                                sqlite3.connect(
                                                                    DB_POSTS_ROOT
                                                                )
                                                            )
                                                            connection.set_trace_callback(
                                                                Log.database
                                                            )  # Set the trace callback for the connection
                                                            cursor = connection.cursor()
                                                            cursor.execute(
                                                                """update posts set Author = ? where author = ? """,
                                                                [
                                                                    (newUserName),
                                                                    (
                                                                        session[
                                                                            "userName"
                                                                        ]
                                                                    ),
                                                                ],
                                                            )
                                                            connection.commit()
                                                            # Update username in comments database
                                                            connection = (
                                                                sqlite3.connect(
                                                                    DB_COMMENTS_ROOT
                                                                )
                                                            )
                                                            connection.set_trace_callback(
                                                                Log.database
                                                            )  # Set the trace callback for the connection
                                                            cursor = connection.cursor()
                                                            cursor.execute(
                                                                """update comments set user = ? where user = ? """,
                                                                [
                                                                    (newUserName),
                                                                    (
                                                                        session[
                                                                            "userName"
                                                                        ]
                                                                    ),
                                                                ],
                                                            )
                                                            connection.commit()
                                                            # Update session username
                                                            session["userName"] = (
                                                                newUserName
                                                            )
                                                            Log.success(
                                                                f'User: "{session["userName"]}" changed his username to "{newUserName}"'
                                                            )
                                                            flashMessage(
                                                                page="changeUserName",
                                                                message="success",
                                                                category="success",
                                                                language=session[
                                                                    "language"
                                                                ],
                                                            )  # Display a flash message
                                                            return redirect(
                                                                f"/user/{newUserName.lower()}"
                                                            )
                                                        case False:
                                                            # Recaptcha verification failed
                                                            Log.error(
                                                                f"Username change reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}"
                                                            )
                                                            abort(401)
                                                case False:
                                                    # Recaptcha not enabled
                                                    cursor.execute(
                                                        """update users set userName = ? where userName = ? """,
                                                        [
                                                            (newUserName),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    # Update username in posts database
                                                    connection = sqlite3.connect(
                                                        DB_POSTS_ROOT
                                                    )
                                                    connection.set_trace_callback(
                                                        Log.database
                                                    )  # Set the trace callback for the connection
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update posts set Author = ? where author = ? """,
                                                        [
                                                            (newUserName),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    # Update username in comments database
                                                    connection = sqlite3.connect(
                                                        DB_COMMENTS_ROOT
                                                    )
                                                    connection.set_trace_callback(
                                                        Log.database
                                                    )  # Set the trace callback for the connection
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update comments set user = ? where user = ? """,
                                                        [
                                                            (newUserName),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    Log.success(
                                                        f'User: "{session["userName"]}" changed his username to "{newUserName}"'
                                                    )
                                                    session["userName"] = newUserName
                                                    flashMessage(
                                                        page="changeUserName",
                                                        message="success",
                                                        category="success",
                                                        language=session["language"],
                                                    )  # Display a flash message
                                                    return redirect(
                                                        f"/user/{newUserName.lower()}"
                                                    )
                                        case False:
                                            # Username already taken
                                            flashMessage(
                                                page="changeUserName",
                                                message="taken",
                                                category="error",
                                                language=session["language"],
                                            )  # Display a flash message
                        case False:
                            flashMessage(
                                page="changeUserName",
                                message="ascii",
                                category="error",
                                language=session["language"],
                            )  # Display a flash message
            # Render the change username template
            return render_template(
                "changeUserName.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            Log.error(
                f"{request.remote_addr} tried to change his username without being logged in"
            )  # Log a message with level 1 indicating the user is not logged in
            # User is not logged in, redirect to homepage
            return redirect("/")
