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
    sha256_crypt,
    RECAPTCHA,
    requestsPost,
    DB_USERS_ROOT,
    render_template,
    changePasswordForm,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_PASSWORD_CHANGE,
)

changePasswordBlueprint = Blueprint("changePassword", __name__)


@changePasswordBlueprint.route("/changepassword", methods=["GET", "POST"])
def changePassword():
    match "userName" in session:
        case True:
            form = changePasswordForm(request.form)
            match request.method == "POST":
                case True:
                    oldPassword = request.form["oldPassword"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select password from users where userName = ? """,
                        [(session["userName"])],
                    )
                    match sha256_crypt.verify(oldPassword, cursor.fetchone()[0]):
                        case True:
                            match oldPassword == password:
                                case True:
                                    flash(
                                        "new password can not be same with old password",
                                        "error",
                                    )
                            match password != passwordConfirm:
                                case True:
                                    flash("passwords must match", "error")
                            match oldPassword != password and password == passwordConfirm:
                                case True:
                                    newPassword = sha256_crypt.hash(password)
                                    connection = sqlite3.connect(DB_USERS_ROOT)
                                    match RECAPTCHA and RECAPTCHA_PASSWORD_CHANGE:
                                        case True:
                                            secretResponse = request.form[
                                                "g-recaptcha-response"
                                            ]
                                            verifyResponse = requestsPost(
                                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                            ).json()
                                            match verifyResponse[
                                                "success"
                                            ] == True or verifyResponse["score"] > 0.5:
                                                case True:
                                                    message("2",f"PASSWORD CHANGE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        """update users set password = ? where userName = ? """,
                                                        [
                                                            (newPassword),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    message(
                                                        "2",
                                                        f'USER: "{session["userName"]}" CHANGED HIS PASSWORD',
                                                    )
                                                    session.clear()
                                                    flash(
                                                        "you need login with new password",
                                                        "success",
                                                    )
                                                    return redirect("/login/redirect=&")
                                                case False:
                                                    message("1",f"PASSWORD CHANGE DELETE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                    abort(401)
                                        case False:
                                            cursor = connection.cursor()
                                            cursor.execute(
                                                        """update users set password = ? where userName = ? """,
                                                        [
                                                            (newPassword),
                                                            (session["userName"]),
                                                        ],
                                                    )
                                            connection.commit()
                                            message(
                                                        "2",
                                                        f'USER: "{session["userName"]}" CHANGED HIS PASSWORD',
                                                    )
                                            session.clear()
                                            flash(
                                                        "you need login with new password",
                                                        "success",
                                                    )
                                            return redirect("/login/redirect=&")
                        case _:
                            flash("old is password wrong", "error")
            return render_template(
                "changePassword.html",
                form=form,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need login for change your password", "error")
            return redirect("/login/redirect=changepassword")
