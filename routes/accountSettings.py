# Import the necessary modules and functions
from modules import (
    abort,
    Delete,
    Log,
    request,
    sqlite3,
    session,
    redirect,
    Blueprint,
    RECAPTCHA,
    requestsPost,
    DB_USERS_ROOT,
    render_template,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_DELETE_USER,
)

# Create a blueprint for the account settings route
accountSettingsBlueprint = Blueprint("accountSettings", __name__)


@accountSettingsBlueprint.route("/accountsettings", methods=["GET", "POST"])
def accountSettings():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            # Connect to the database and get the user name
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select userName from users where userName = ? """,
                [(session["userName"])],
            )
            user = cursor.fetchall()
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Check if recaptcha is enabled and required for deleting user
                    match RECAPTCHA and RECAPTCHA_DELETE_USER:
                        case True:
                            # Get the recaptcha response from the form
                            secretResponse = request.form["g-recaptcha-response"]
                            # Verify the recaptcha response with the recaptcha API
                            verifyResponse = requestsPost(
                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                            ).json()
                            # Check if the recaptcha verification is successful or has a high score
                            match verifyResponse["success"] == True or verifyResponse[
                                "score"
                            ] > 0.5:

                                case True:
                                    # Log the recaptcha verification result
                                    Log.success(
                                        "2",
                                        f"USER DELETE RECAPTCHA | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
                                    )
                                    # Delete the user from the database
                                    Delete.user(user[0][0])
                                    # Redirect to the home page
                                    return redirect(f"/")
                                case False:
                                    # Log the recaptcha verification result
                                    Log.danger(
                                        f"USER DELETE RECAPTCHA | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
                                    )
                                    # Abort the request with a 401 error
                                    abort(401)
                        case False:
                            # Delete the user from the database
                            Delete.user(user[0][0])
                            # Redirect to the home page
                            return redirect(f"/")
            # Render the account settings template with the user and recaptcha data
            return render_template(
                "accountSettings.html.jinja",
                user=user,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            # Redirect to the login page with the account settings as the next destination
            return redirect("/login/redirect=&accountsettings")
