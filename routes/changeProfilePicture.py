# Import the necessary modules and functions
from helpers import (
    abort,
    flash,
    session,
    sqlite3,
    request,
    message,
    redirect,
    Blueprint,
    RECAPTCHA,
    requestsPost,
    DB_USERS_ROOT,
    render_template,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    ChangeProfilePictureForm,
    RECAPTCHA_PROFILE_PICTURE_CHANGE,
)

# Create a blueprint for the change profile picture route
changeProfilePictureBlueprint = Blueprint("changeProfilePicture", __name__)


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
                    # Connect to the users database
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    # Check if recaptcha is enabled and required for changing profile picture
                    match RECAPTCHA and RECAPTCHA_PROFILE_PICTURE_CHANGE:
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
                                    message(
                                        "2",
                                        f"CHANGE PROFILE PICTURE RECAPTCHA | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
                                    )
                                    # Update the users database by setting the new profile picture for the user name
                                    cursor.execute(
                                        """update users set profilePicture = ? where userName = ? """,
                                        [(newProfilePicture), (session["userName"])],
                                    )
                                    connection.commit()
                                    # Log a message that the user changed their profile picture
                                    message(
                                        "2",
                                        f'USER: "{session["userName"]}" CHANGED HIS PROFILE PICTURE TO "{newProfilePicture}"',
                                    )
                                    # Flash a success message to the user
                                    flash("profile picture changed", "success")
                                    # Redirect to the same route
                                    return redirect(f"/changeprofilepicture")
                                case False:
                                    # Log the recaptcha verification result
                                    message(
                                        "1",
                                        f"CHANGE PROFILE PICTURE RECAPTCHA | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
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
                            message(
                                "2",
                                f'USER: "{session["userName"]}" CHANGED HIS PROFILE PICTURE TO "{newProfilePicture}"',
                            )
                            # Flash a success message to the user
                            flash("profile picture changed", "success")
                            # Redirect to the same route
                            return redirect(f"/changeprofilepicture")
            # Render the change profile picture template with the form object, the site key and the recaptcha flag
            return render_template(
                "changeProfilePicture.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            # Redirect to the home page if the user is not logged in
            return redirect("/")
