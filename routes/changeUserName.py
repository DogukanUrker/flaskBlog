from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
    changeUserNameForm,
)

changeUserNameBlueprint = Blueprint("changeUserName", __name__)


@changeUserNameBlueprint.route("/changeusername", methods=["GET", "POST"])
def changeUserName():
    match "userName" in session:
        case True:
            form = changeUserNameForm(request.form)
            if request.method == "POST":
                newUserName = request.form["newUserName"]
                newUserName = newUserName.replace(" ", "")
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'select userName from users where userName = "{newUserName}"'
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
                                        cursor.execute(
                                            f'update users set userName = "{newUserName}" where userName = "{session["userName"]}" '
                                        )
                                        connection.commit()
                                        connection = sqlite3.connect("db/posts.db")
                                        cursor = connection.cursor()
                                        cursor.execute(
                                            f'update posts set Author = "{newUserName}" where author = "{session["userName"]}" '
                                        )
                                        connection.commit()
                                        connection = sqlite3.connect("db/comments.db")
                                        cursor = connection.cursor()
                                        cursor.execute(
                                            f'update comments set user = "{newUserName}" where user = "{session["userName"]}" '
                                        )
                                        connection.commit()
                                        message(
                                            "2",
                                            f'USER: "{session["userName"]}" CHANGED USER NAME TO "{newUserName}"',
                                        )
                                        session["userName"] = newUserName
                                        flash("user name changed", "success")
                                        return redirect(f"/user/{newUserName.lower()}")
                                    case False:
                                        flash(
                                            "This username is already taken.", "error"
                                        )
                    case False:
                        flash("username does not fit ascii charecters", "error")

            return render_template("changeUserName.html", form=form)
        case False:
            return redirect("/")
