# Import necessary modules and functions
from modules import (
    DB_USERS_ROOT,  # Path to the users database
    RECAPTCHA,  # Flag indicating if reCAPTCHA is enabled
    RECAPTCHA_PROFILE_PICTURE_CHANGE,  # Flag indicating if reCAPTCHA is required for changing profile picture
    RECAPTCHA_SECRET_KEY,  # reCAPTCHA secret key
    RECAPTCHA_SITE_KEY,  # reCAPTCHA site key
    RECAPTCHA_VERIFY_URL,  # reCAPTCHA verification URL
    Blueprint,  # Blueprint for defining routes
    ChangeProfilePictureForm,  # Form for changing profile picture
    Log,  # Custom logging module
    abort,  # Function to abort request
    flashMessage,  # Flash messaging module
    redirect,  # Redirect function
    render_template,  # Template rendering function
    request,  # Request handling module
    requestsPost,  # Function for making HTTP POST requests
    session,  # Session handling module
    sqlite3,  # SQLite database module
)

# Create a blueprint for the change profile picture route
changeProfilePictureBlueprint = Blueprint("changeProfilePicture", __name__)


# Define a route for changing profile picture
@changeProfilePictureBlueprint.route("/changeprofilepicture", methods=["GET", "POST"])
def changeProfilePicture():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            # Create a change profile picture form object from the request form
            form = ChangeProfilePictureForm(request.form)
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Get the new profile picture seed from the form
                    newProfilePictureSeed = request.form["newProfilePictureSeed"]
                    # Generate the new profile picture URL from the seed
                    newProfilePicture = f"https://api.dicebear.com/7.x/identicon/svg?seed={newProfilePictureSeed}&radius=10"
                    Log.sql(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    Log.sql(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the users database
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    # Check if reCAPTCHA is enabled and required for changing profile picture
                    match RECAPTCHA and RECAPTCHA_PROFILE_PICTURE_CHANGE:
                        case True:
                            # Get the reCAPTCHA response from the form
                            secretResponse = request.form["g-recaptcha-response"]
                            # Verify the reCAPTCHA response with the reCAPTCHA API
                            verifyResponse = requestsPost(
                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                            ).json()
                            # Check if the reCAPTCHA verification is successful or has a high score
                            match (
                                verifyResponse["success"] is True
                                or verifyResponse["score"] > 0.5
                            ):
                                case True:
                                    # Log the reCAPTCHA verification result
                                    Log.success(
                                        f"Change profile picture reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )
                                    # Update the users database by setting the new profile picture for the user name
                                    cursor.execute(
                                        """update users set profilePicture = ? where userName = ? """,
                                        [(newProfilePicture), (session["userName"])],
                                    )
                                    connection.commit()
                                    # Log a message that the user changed their profile picture
                                    Log.success(
                                        f'User: "{session["userName"]}" changed his profile picture to "{newProfilePicture}"',
                                    )
                                    flashMessage(
                                        page="changeProfilePicture",
                                        message="success",
                                        category="success",
                                        language=session["language"],
                                    )  # Display a flash message
                                    # Redirect to the same route
                                    return redirect("/changeprofilepicture")
                                case False:
                                    # Log the reCAPTCHA verification result
                                    Log.danger(
                                        f"Change profile picture reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )
                                    # Abort the request with a 401 error
                                    abort(401)
                        case False:
                            # Update the users database by setting the new profile picture for the user name
                            cursor.execute(
                                """update users set profilePicture = ? where userName = ? """,
                                [(newProfilePicture), (session["userName"])],
                            )
                            connection.commit()
                            # Log a message that the user changed their profile picture
                            Log.success(
                                f'User: "{session["userName"]}" changed his profile picture to "{newProfilePicture}"',
                            )
                            flashMessage(
                                page="changeProfilePicture",
                                message="success",
                                category="success",
                                language=session["language"],
                            )  # Display a flash message
                            # Redirect to the same route
                            return redirect("/changeprofilepicture")
            # Render the change profile picture template with the form object, the site key, and the reCAPTCHA flag
            return render_template(
                "changeProfilePicture.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            Log.danger(
                f"{request.remote_addr} tried to change his profile picture without being logged in"
            )  # Log a message with level 1 indicating the user is not logged in
            # Redirect to the home page if the user is not logged in
            return redirect("/")
