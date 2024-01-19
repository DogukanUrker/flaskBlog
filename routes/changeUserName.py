from helpers import (
    flash,
    abort,
    message,
    session,
    sqlite3,
    request,
    message,
    redirect,
    Blueprint,
    RECAPTCHA,
    requestsPost,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    render_template,
    DB_COMMENTS_ROOT,
    changeUserNameForm,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_USERNAME_CHANGE,
)

changeUserNameBlueprint = Blueprint("changeUserName", __name__)


@changeUserNameBlueprint.route("/changeusername", methods=["GET", "POST"])
def changeUserName():
    match "userName" in session:
        case True:
            form = changeUserNameForm(request.form)
            match request.method == "POST":
                case True:
                    newUserName = request.form["newUserName"]
                    newUserName = newUserName.replace(" ", "")
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select userName from users where userName = ? """,
                        [(newUserName)],
                    )
                    userNameCheck = cursor.fetchone()
                    match newUserName.isascii():
                        case True:
                            match newUserName == session["userName"]:
                                case True:
                                    flash("this is your username", "error")
                                case False:
                                    match userNameCheck == None:
                                        case True:
                                            match RECAPTCHA and RECAPTCHA_USERNAME_CHANGE:
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
                                                            message("2",f"USERNAME CHANGE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
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
                                                            connection = (
                                                                sqlite3.connect(
                                                                    DB_POSTS_ROOT
                                                                )
                                                            )
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
                                                            connection = (
                                                                sqlite3.connect(
                                                                    DB_COMMENTS_ROOT
                                                                )
                                                            )
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
                                                            message(
                                                                "2",
                                                                f'USER: "{session["userName"]}" CHANGED USER NAME TO "{newUserName}"',
                                                            )
                                                            session[
                                                                "userName"
                                                            ] = newUserName
                                                            flash(
                                                                "user name changed",
                                                                "success",
                                                            )
                                                            return redirect(
                                                                f"/user/{newUserName.lower()}"
                                                            )
                                                        case False:
                                                            message("1",f"USERNAME CHANGE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            abort(401)
                                                case False:
                                                    cursor.execute(
                                                        """update users set userName = ? where userName = ? """,
                                                        [
                                                            (newUserName),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    connection = sqlite3.connect(
                                                        DB_POSTS_ROOT
                                                    )
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update posts set Author = ? where author = ? """,
                                                        [
                                                            (newUserName),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    connection = sqlite3.connect(
                                                        DB_COMMENTS_ROOT
                                                    )
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update comments set user = ? where user = ? """,
                                                        [
                                                            (newUserName),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    message(
                                                        "2",
                                                        f'USER: "{session["userName"]}" CHANGED USER NAME TO "{newUserName}"',
                                                    )
                                                    session["userName"] = newUserName
                                                    flash(
                                                        "user name changed", "success"
                                                    )
                                                    return redirect(
                                                        f"/user/{newUserName.lower()}"
                                                    )
                                        case False:
                                            flash(
                                                "This username is already taken.",
                                                "error",
                                            )
                        case False:
                            flash("username does not fit ascii charecters", "error")
            return render_template(
                "changeUserName.html",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            return redirect("/")
