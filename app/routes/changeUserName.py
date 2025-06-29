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
    DB_COMMENTS_ROOT,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_USERNAME_CHANGE,
    RECAPTCHA_VERIFY_URL,
)
from utils.flashMessage import flashMessage
from utils.forms.ChangeUserNameForm import ChangeUserNameForm
from utils.log import Log

changeUserNameBlueprint = Blueprint("changeUserName", __name__)


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

    if "userName" in session:
        form = ChangeUserNameForm(request.form)

        if request.method == "POST":
            newUserName = request.form["newUserName"]
            newUserName = newUserName.replace(" ", "")
            Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()
            cursor.execute(
                """select userName from users where userName = ? """,
                [(newUserName)],
            )
            userNameCheck = cursor.fetchone()

            if newUserName.isascii():
                if newUserName == session["userName"]:
                    flashMessage(
                        page="changeUserName",
                        message="same",
                        category="error",
                        language=session["language"],
                    )
                else:
                    if userNameCheck is None:
                        if RECAPTCHA and RECAPTCHA_USERNAME_CHANGE:
                            secretResponse = request.form["g-recaptcha-response"]
                            verifyResponse = requestsPost(
                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                            ).json()

                            if (
                                verifyResponse["success"] is True
                                or verifyResponse["score"] > 0.5
                            ):
                                Log.success(
                                    f"Change username reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                )

                                cursor.execute(
                                    """update users set userName = ? where userName = ? """,
                                    [(newUserName), (session["userName"])],
                                )
                                connection.commit()

                                connection = sqlite3.connect(DB_POSTS_ROOT)
                                connection.set_trace_callback(Log.database)
                                cursor = connection.cursor()
                                cursor.execute(
                                    """update posts set Author = ? where author = ? """,
                                    [(newUserName), (session["userName"])],
                                )
                                connection.commit()

                                connection = sqlite3.connect(DB_COMMENTS_ROOT)
                                connection.set_trace_callback(Log.database)
                                cursor = connection.cursor()
                                cursor.execute(
                                    """update comments set user = ? where user = ? """,
                                    [(newUserName), (session["userName"])],
                                )
                                connection.commit()

                                session["userName"] = newUserName
                                Log.success(
                                    f'User: "{session["userName"]}" changed his username to "{newUserName}"'
                                )
                                flashMessage(
                                    page="changeUserName",
                                    message="success",
                                    category="success",
                                    language=session["language"],
                                )
                                return redirect(f"/user/{newUserName.lower()}")
                            else:
                                Log.error(
                                    f"Username change reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}"
                                )
                                abort(401)
                        else:
                            cursor.execute(
                                """update users set userName = ? where userName = ? """,
                                [(newUserName), (session["userName"])],
                            )
                            connection.commit()

                            connection = sqlite3.connect(DB_POSTS_ROOT)
                            connection.set_trace_callback(Log.database)
                            cursor = connection.cursor()
                            cursor.execute(
                                """update posts set Author = ? where author = ? """,
                                [(newUserName), (session["userName"])],
                            )
                            connection.commit()

                            connection = sqlite3.connect(DB_COMMENTS_ROOT)
                            connection.set_trace_callback(Log.database)
                            cursor = connection.cursor()
                            cursor.execute(
                                """update comments set user = ? where user = ? """,
                                [(newUserName), (session["userName"])],
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
                            )
                            return redirect(f"/user/{newUserName.lower()}")
                    else:
                        flashMessage(
                            page="changeUserName",
                            message="taken",
                            category="error",
                            language=session["language"],
                        )
            else:
                flashMessage(
                    page="changeUserName",
                    message="ascii",
                    category="error",
                    language=session["language"],
                )

        return render_template(
            "changeUserName.html.jinja",
            form=form,
            siteKey=RECAPTCHA_SITE_KEY,
            recaptcha=RECAPTCHA,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to change his username without being logged in"
        )

        return redirect("/")
