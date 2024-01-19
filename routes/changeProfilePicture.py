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
    changeProfilePictureForm,
    RECAPTCHA_PROFILE_PICTURE_CHANGE,
)

changeProfilePictureBlueprint = Blueprint("changeProfilePicture", __name__)


@changeProfilePictureBlueprint.route("/changeprofilepicture", methods=["GET", "POST"])
def changeProfilePicture():
    match "userName" in session:
        case True:
            form = changeProfilePictureForm(request.form)
            match request.method == "POST":
                case True:
                    newProfilePictureSeed = request.form["newProfilePictureSeed"]
                    newProfilePicture = f"https://api.dicebear.com/7.x/identicon/svg?seed={newProfilePictureSeed}&radius=10"
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    match RECAPTCHA and RECAPTCHA_PROFILE_PICTURE_CHANGE:
                        case True:
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
                                    message("2",f"CHANGE PROFILE PICTURE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                    cursor.execute(
                                        """update users set profilePicture = ? where userName = ? """,
                                        [(newProfilePicture), (session["userName"])],
                                    )
                                    connection.commit()
                                    message(
                                        "2",
                                        f'USER: "{session["userName"]}" CHANGED HIS PROFILE PICTURE TO "{newProfilePicture}"',
                                    )
                                    flash("profile picture changed", "success")
                                    return redirect(f"/changeprofilepicture")
                                case False:
                                    message("1",f"CHANGE PROFILE PICTURE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                    abort(401)
                        case False:
                            cursor.execute(
                                        """update users set profilePicture = ? where userName = ? """,
                                        [(newProfilePicture), (session["userName"])],
                                    )
                            connection.commit()
                            message(
                                        "2",
                                        f'USER: "{session["userName"]}" CHANGED HIS PROFILE PICTURE TO "{newProfilePicture}"',
                                    )
                            flash("profile picture changed", "success")
                            return redirect(f"/changeprofilepicture")
            return render_template(
                "changeProfilePicture.html",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            return redirect("/")
