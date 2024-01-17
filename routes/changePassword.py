from helpers import (
    flash,
    session,
    sqlite3,
    request,
    message,
    redirect,
    Blueprint,
    sha256_crypt,
    DB_USERS_ROOT,
    render_template,
    changePasswordForm,
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
                                    cursor = connection.cursor()
                                    cursor.execute(
                                        """update users set password = ? where userName = ? """,
                                        [(newPassword), (session["userName"])],
                                    )
                                    connection.commit()
                                    message(
                                        "2",
                                        f'USER: "{session["userName"]}" CHANGED HIS PASSWORD',
                                    )
                                    session.clear()
                                    flash("you need login with new password", "success")
                                    return redirect("/login/redirect=&")
                        case _:
                            flash("old is password wrong", "error")
            return render_template("changePassword.html", form=form)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need login for change your password", "error")
            return redirect("/login/redirect=changepassword")
