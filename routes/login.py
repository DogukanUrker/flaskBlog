from helpers import (
    flash,
    url_for,
    session,
    request,
    sqlite3,
    message,
    redirect,
    addPoints,
    Blueprint,
    loginForm,
    sha256_crypt,
    DB_USERS_ROOT,
    render_template,
)
from constants import LOG_IN

loginBlueprint = Blueprint("login", __name__)


@loginBlueprint.route("/login/redirect=<direct>", methods=["GET", "POST"])
def login(direct):
    direct = direct.replace("&", "/")
    match LOG_IN:
        case True:
            match "userName" in session:
                case True:
                    message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
                    return (
                        redirect(direct),
                        301,
                    )
                case False:
                    form = loginForm(request.form)
                    match request.method == "POST":
                        case True:
                            userName = request.form["userName"]
                            password = request.form["password"]
                            userName = userName.replace(" ", "")
                            connection = sqlite3.connect(DB_USERS_ROOT)
                            cursor = connection.cursor()
                            cursor.execute(
                                """select * from users where lower(userName) = ? """,
                                [(userName.lower())],
                            )
                            user = cursor.fetchone()
                            match not user:
                                case True:
                                    message("1", f'USER: "{userName}" NOT FOUND')
                                    flash("user not found", "error")
                                case _:
                                    match sha256_crypt.verify(password, user[3]):
                                        case True:
                                            session["userName"] = user[1]
                                            addPoints(1, session["userName"])
                                            message("2", f'USER: "{user[1]}" LOGGED IN')
                                            flash(f"Welcome {user[1]}", "success")
                                            return (
                                                redirect(direct),
                                                301,
                                            )
                                        case _:
                                            message("1", "WRONG PASSWORD")
                                            flash("wrong  password", "error")
                    return render_template("login.html", form=form, hideLogin=True)
        case False:
            return (
                redirect(direct),
                301,
            )
