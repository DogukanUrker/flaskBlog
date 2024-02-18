# Import necessary modules and functions
from modules import (
    Log,  # A class for logging messages
    abort,  # Function to abort the request
    Delete,  # Function to delete user from the database
    request,  # Module for handling HTTP requests
    sqlite3,  # SQLite database module
    session,  # Session handling module
    redirect,  # Function to redirect
    Blueprint,  # Blueprint for defining routes
    RECAPTCHA,  # Flag indicating whether reCAPTCHA is enabled
    requestsPost,  # Function to make POST requests
    DB_USERS_ROOT,  # Path to the users database
    render_template,  # Function to render HTML templates
    RECAPTCHA_SITE_KEY,  # reCAPTCHA site key
    RECAPTCHA_VERIFY_URL,  # reCAPTCHA verification URL
    RECAPTCHA_SECRET_KEY,  # reCAPTCHA secret key
    RECAPTCHA_DELETE_USER,  # Flag indicating whether reCAPTCHA is required for deleting user
)

# Create a blueprint for the account settings route
accountSettingsBlueprint = Blueprint("accountSettings", __name__)


# Define route for account settings
@accountSettingsBlueprint.route("/accountsettings", methods=["GET", "POST"])
def accountSettings():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            Log.sql(
                f"Connecting to '{DB_USERS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the database and get the user name
            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = connection.cursor()
            cursor.execute(
                """select userName from users where userName = ? """,
                [(session["userName"])],
            )
            user = cursor.fetchall()
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Check if reCAPTCHA is enabled and required for deleting user
                    match RECAPTCHA and RECAPTCHA_DELETE_USER:
                        case True:
                            # Get the reCAPTCHA response from the form
                            secretResponse = request.form["g-recaptcha-response"]
                            # Verify the reCAPTCHA response with the reCAPTCHA API
                            verifyResponse = requestsPost(
                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                            ).json()
                            # Check if the reCAPTCHA verification is successful or has a high score
                            match verifyResponse["success"] == True or verifyResponse[
                                "score"
                            ] > 0.5:
                                case True:
                                    # Log the reCAPTCHA verification result
                                    Log.success(
                                        f"User delete reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )
                                    # Delete the user from the database
                                    Delete.user(user[0][0])
                                    # Redirect to the home page
                                    return redirect(f"/")
                                case False:
                                    # Log the reCAPTCHA verification result
                                    Log.danger(
                                        f"User delete reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )
                                    # Abort the request with a 401 error
                                    abort(401)
                        case False:
                            # Delete the user from the database
                            Delete.user(user[0][0])
                            # Redirect to the home page
                            return redirect(f"/")
            # Render the account settings template with the user and reCAPTCHA data
            return render_template(
                "accountSettings.html.jinja",
                user=user,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            Log.danger(
                f"{request.remote_addr} tried to reach account settings without being logged in"
            )  # Log a message with level 1 indicating the user is not logged in
            # Redirect to the login page with the account settings as the next destination
            return redirect("/login/redirect=&accountsettings")
