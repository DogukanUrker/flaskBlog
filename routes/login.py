# Import necessary modules and functions
from modules import (
    Log,  # Custom logging module
    abort,  # Function to abort request processing
    flash,  # Flash messaging module
    LOG_IN,  # Flag indicating if login is enabled
    session,  # Session handling module
    request,  # Request handling module
    sqlite3,  # SQLite database module
    redirect,  # Redirect function
    RECAPTCHA,  # Flag for enabling reCAPTCHA
    addPoints,  # Function to add points to user's score
    Blueprint,  # Blueprint for defining routes
    LoginForm,  # Form class for login
    encryption,  # Encryption utility module
    requestsPost,  # Function for making POST requests
    DB_USERS_ROOT,  # Path to the users database
    render_template,  # Template rendering function
    RECAPTCHA_LOGIN,  # Flag for enabling reCAPTCHA for login
    RECAPTCHA_SITE_KEY,  # reCAPTCHA site key
    RECAPTCHA_VERIFY_URL,  # reCAPTCHA verification URL
    RECAPTCHA_SECRET_KEY,  # reCAPTCHA secret key
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
                    Log.danger(f'User: "{session["userName"]}" already logged in')
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
                            Log.sql(
                                f"Connecting to '{DB_USERS_ROOT}' database"
                            )  # Log the database connection is started
                            connection = sqlite3.connect(DB_USERS_ROOT)
                            connection.set_trace_callback(
                                Log.sql
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
                                    Log.danger(f'User: "{userName}" not found')
                                    flash("User not found.", "error")
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
                                                    match verifyResponse[
                                                        "success"
                                                    ] == True or verifyResponse[
                                                        "score"
                                                    ] > 0.5:
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
                                                                f'USER: "{user[1]}" LOGGED IN',
                                                            )
                                                            flash(
                                                                f"Welcome, {user[1]}!",
                                                                "success",
                                                            )
                                                            return (
                                                                redirect(direct),
                                                                301,
                                                            )

                                                        case False:
                                                            # Returns an unauthorized error if the reCAPTCHA verification is unsuccessful
                                                            Log.danger(
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
                                                    flash(
                                                        f"Welcome, {user[1]}!",
                                                        "success",
                                                    )
                                                    return (
                                                        redirect(direct),
                                                        301,
                                                    )

                                        case _:
                                            # Returns an incorrect password error if the password is incorrect
                                            Log.danger("Wrong password")
                                            flash("Wrong password.", "error")
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
