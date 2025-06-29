# Import necessary modules and functions
from modules import (
    DB_USERS_ROOT,  # Path to the users database
    LOG_IN,  # Flag indicating if login is enabled
    RECAPTCHA,  # Flag for enabling reCAPTCHA
    RECAPTCHA_LOGIN,  # Flag for enabling reCAPTCHA for login
    RECAPTCHA_SECRET_KEY,  # reCAPTCHA secret key
    RECAPTCHA_SITE_KEY,  # reCAPTCHA site key
    RECAPTCHA_VERIFY_URL,  # reCAPTCHA verification URL
    Blueprint,  # Blueprint for defining routes
    Log,  # Custom logging module
    LoginForm,  # Form class for login
    abort,  # Function to abort request processing
    addPoints,  # Function to add points to user's score
    encryption,  # Encryption utility module
    flashMessage,  # Flash messaging module
    redirect,  # Redirect function
    render_template,  # Template rendering function
    request,  # Request handling module
    requestsPost,  # Function for making POST requests
    session,  # Session handling module
    sqlite3,  # SQLite database module
)

# Create a blueprint for the login route
loginBlueprint = Blueprint("login", __name__)


# Define a route for login
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
    direct = direct.replace("&", "/")  # Convert direct link parameter
    match LOG_IN:
        case True:
            match "userName" in session:
                case True:
                    # If user is already logged in, redirect
                    Log.error(f'User: "{session["userName"]}" already logged in')
                    return (
                        redirect(direct),
                        301,
                    )
                case False:
                    form = LoginForm(request.form)
                    match request.method == "POST":
                        case True:
                            # Retrieve form data
                            userName = request.form["userName"]
                            password = request.form["password"]
                            userName = userName.replace(" ", "")
                            Log.database(
                                f"Connecting to '{DB_USERS_ROOT}' database"
                            )  # Log the database connection is started
                            connection = sqlite3.connect(DB_USERS_ROOT)
                            connection.set_trace_callback(
                                Log.database
                            )  # Set the trace callback for the connection
                            cursor = connection.cursor()
                            cursor.execute(
                                """select * from users where lower(userName) = ? """,
                                [(userName.lower())],
                            )
                            user = cursor.fetchone()
                            match not user:
                                case True:
                                    # If user not found, show error message
                                    Log.error(f'User: "{userName}" not found')
                                    flashMessage(
                                        page="login",
                                        message="notFound",
                                        category="error",
                                        language=session["language"],
                                    )  # Display a flash message
                                case _:
                                    match encryption.verify(password, user[3]):
                                        case True:
                                            match RECAPTCHA and RECAPTCHA_LOGIN:
                                                case True:
                                                    # Perform reCAPTCHA verification
                                                    secretResponse = request.form[
                                                        "g-recaptcha-response"
                                                    ]
                                                    verifyResponse = requestsPost(
                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                    ).json()
                                                    match (
                                                        verifyResponse["success"]
                                                        is True
                                                        or verifyResponse["score"] > 0.5
                                                    ):
                                                        case True:
                                                            # Logs the user in if the reCAPTCHA verification is successful
                                                            Log.success(
                                                                f"Login reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            session["userName"] = user[
                                                                1
                                                            ]
                                                            session["userRole"] = user[
                                                                5
                                                            ]
                                                            addPoints(
                                                                1, session["userName"]
                                                            )
                                                            Log.success(
                                                                f'User: "{user[1]}" logged in',
                                                            )
                                                            flashMessage(
                                                                page="login",
                                                                message="success",
                                                                category="success",
                                                                language=session[
                                                                    "language"
                                                                ],
                                                            )  # Display a flash message

                                                            return (
                                                                redirect(direct),
                                                                301,
                                                            )

                                                        case False:
                                                            # Returns an unauthorized error if the reCAPTCHA verification is unsuccessful
                                                            Log.error(
                                                                f"Login reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)

                                                case False:
                                                    # Logs the user in if reCAPTCHA is not required
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
                                                    )  # Display a flash message

                                                    return (
                                                        redirect(direct),
                                                        301,
                                                    )

                                        case _:
                                            # Returns an incorrect password error if the password is incorrect
                                            Log.error("Wrong password")
                                            flashMessage(
                                                page="login",
                                                message="password",
                                                category="error",
                                                language=session["language"],
                                            )  # Display a flash message
                    # Render login template with appropriate form and messages
                    return render_template(
                        "login.html.jinja",
                        form=form,
                        hideLogin=True,
                        siteKey=RECAPTCHA_SITE_KEY,
                        recaptcha=RECAPTCHA,
                    )
        case False:
            return (
                redirect(direct),
                301,
            )
