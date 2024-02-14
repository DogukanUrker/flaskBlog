# Import necessary modules and functions
from modules import (
    Log,  # Logging module
    flash,  # Flash messaging module
    abort,  # Function for aborting requests
    session,  # Session management module
    sqlite3,  # SQLite database module
    request,  # Module for handling HTTP requests
    redirect,  # Function for redirecting requests
    Blueprint,  # Blueprint class for creating modular applications
    RECAPTCHA,  # Recaptcha module
    requestsPost,  # Module for making HTTP POST requests
    DB_POSTS_ROOT,  # Path to the posts database
    DB_USERS_ROOT,  # Path to the users database
    render_template,  # Function for rendering templates
    DB_COMMENTS_ROOT,  # Path to the comments database
    ChangeUserNameForm,  # Form for changing user name
    RECAPTCHA_SITE_KEY,  # Recaptcha site key
    RECAPTCHA_VERIFY_URL,  # Recaptcha verification URL
    RECAPTCHA_SECRET_KEY,  # Recaptcha secret key
    RECAPTCHA_USERNAME_CHANGE,  # Flag for enabling/disabling Recaptcha for username change
)

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
                    Log.sql(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the users database
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
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
                                    flash(
                                        "This is your username.", "error"
                                    )  # Flash an error message
                                case False:
                                    # Check if new username is available
                                    match userNameCheck == None:
                                        case True:
                                            # Check Recaptcha if enabled
                                            match RECAPTCHA and RECAPTCHA_USERNAME_CHANGE:
                                                case True:
                                                    # Verify Recaptcha response
                                                    secretResponse = request.form[
                                                        "g-recaptcha-response"
                                                    ]
                                                    verifyResponse = requestsPost(
                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                    ).json()
                                                    # Check Recaptcha verification result
                                                    match verifyResponse[
                                                        "success"
                                                    ] == True or verifyResponse[
                                                        "score"
                                                    ] > 0.5:
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
                                                                Log.sql
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
                                                                Log.sql
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
                                                            flash(
                                                                "Username changed.",
                                                                "success",
                                                            )
                                                            return redirect(
                                                                f"/user/{newUserName.lower()}"
                                                            )
                                                        case False:
                                                            # Recaptcha verification failed
                                                            Log.danger(
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
                                                        Log.sql
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
                                                        Log.sql
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
                                                    flash(
                                                        "Username changed.", "success"
                                                    )
                                                    return redirect(
                                                        f"/user/{newUserName.lower()}"
                                                    )
                                        case False:
                                            # Username already taken
                                            flash(
                                                "This username is already taken.",
                                                "error",
                                            )
                        case False:
                            # Username contains non-ASCII characters
                            flash("Username contains non-ASCII characters.", "error")
            # Render the change username template
            return render_template(
                "changeUserName.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            Log.danger(
                f"{request.remote_addr} tried to change his username without being logged in"
            )  # Log a message with level 1 indicating the user is not logged in
            # User is not logged in, redirect to homepage
            return redirect("/")
