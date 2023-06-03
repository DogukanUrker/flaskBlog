from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
    sha256_crypt,
    changePasswordForm,
)

changePasswordBlueprint = Blueprint("changePassword", __name__)


@changePasswordBlueprint.route("/changepassword", methods=["GET", "POST"])
def changePassword():
    match "userName" in session:
        case True:
            form = changePasswordForm(request.form)
            if request.method == "POST":
                oldPassword = request.form["oldPassword"]
                password = request.form["password"]
                passwordConfirm = request.form["passwordConfirm"]
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'select password from users where userName = "{session["userName"]}"'
                )
                if sha256_crypt.verify(oldPassword, cursor.fetchone()[0]):
                    if oldPassword == password:
                        flash("new password can not be same with old password", "error")
                    elif password != passwordConfirm:
                        flash("passwords must match", "error")
                    elif oldPassword != password and password == passwordConfirm:
                        newPassword = sha256_crypt.hash(password)
                        connection = sqlite3.connect("db/users.db")
                        cursor = connection.cursor()
                        cursor.execute(
                            f'update users set password = "{newPassword}" where userName = "{session["userName"]}"'
                        )
                        connection.commit()
                        message(
                            "2", f'USER: "{session["userName"]}" CHANGED HIS PASSWORD'
                        )
                        session.clear()
                        flash("you need login with new password", "success")
                        return redirect("/login/redirect=&")
                else:
                    flash("old password wrong", "error")

            return render_template("changePassword.html", form=form)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need login for change your password", "error")
            return redirect("/login/redirect=changepassword")
