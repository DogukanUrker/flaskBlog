import sqlite3

from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    session,
)
from requests import post as requestsPost
from settings import (
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_PROFILE_PICTURE_CHANGE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.flashMessage import flashMessage
from utils.forms.ChangeProfilePictureForm import ChangeProfilePictureForm
from utils.log import Log

changeProfilePictureBlueprint = Blueprint("changeProfilePicture", __name__)


@changeProfilePictureBlueprint.route("/changeprofilepicture", methods=["GET", "POST"])
def changeProfilePicture():
    match "userName" in session:
        case True:
            form = ChangeProfilePictureForm(request.form)

            match request.method == "POST":
                case True:
                    newProfilePictureSeed = request.form["newProfilePictureSeed"]

                    newProfilePicture = f"https://api.dicebear.com/7.x/identicon/svg?seed={newProfilePictureSeed}&radius=10"
                    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")
                    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(Log.database)
                    cursor = connection.cursor()

                    match RECAPTCHA and RECAPTCHA_PROFILE_PICTURE_CHANGE:
                        case True:
                            secretResponse = request.form["g-recaptcha-response"]

                            verifyResponse = requestsPost(
                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                            ).json()

                            match (
                                verifyResponse["success"] is True
                                or verifyResponse["score"] > 0.5
                            ):
                                case True:
                                    Log.success(
                                        f"Change profile picture reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )

                                    cursor.execute(
                                        """update users set profilePicture = ? where userName = ? """,
                                        [(newProfilePicture), (session["userName"])],
                                    )
                                    connection.commit()

                                    Log.success(
                                        f'User: "{session["userName"]}" changed his profile picture to "{newProfilePicture}"',
                                    )
                                    flashMessage(
                                        page="changeProfilePicture",
                                        message="success",
                                        category="success",
                                        language=session["language"],
                                    )

                                    return redirect("/changeprofilepicture")
                                case False:
                                    Log.error(
                                        f"Change profile picture reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )

                                    abort(401)
                        case False:
                            cursor.execute(
                                """update users set profilePicture = ? where userName = ? """,
                                [(newProfilePicture), (session["userName"])],
                            )
                            connection.commit()

                            Log.success(
                                f'User: "{session["userName"]}" changed his profile picture to "{newProfilePicture}"',
                            )
                            flashMessage(
                                page="changeProfilePicture",
                                message="success",
                                category="success",
                                language=session["language"],
                            )

                            return redirect("/changeprofilepicture")

            return render_template(
                "changeProfilePicture.html.jinja",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            Log.error(
                f"{request.remote_addr} tried to change his profile picture without being logged in"
            )

            return redirect("/")
