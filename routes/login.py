from helpers import (
    flash,
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
                    return redirect(direct)
                case False:
                    form = loginForm(request.form)
                    if request.method == "POST":
                        userName = request.form["userName"]
                        password = request.form["password"]
                        userName = userName.replace(" ", "")
                        connection = sqlite3.connect(DB_USERS_ROOT)
                        cursor = connection.cursor()
                        cursor.execute(
                            f'select * from users where lower(userName) = "{userName.lower()}"'
                        )
                        user = cursor.fetchone()
                        if not user:
                            message("1", f'USER: "{userName}" NOT FOUND')
                            flash("user not found", "error")
                        else:
                            if sha256_crypt.verify(password, user[3]):
                                session["userName"] = user[1]
                                addPoints(1, session["userName"])
                                message("2", f'USER: "{user[1]}" LOGGED IN')
                                flash(f"Welcome {user[1]}", "success")
                                return redirect(direct)
                            else:
                                message("1", "WRONG PASSWORD")
                                flash("wrong  password", "error")
                    return render_template("login.html", form=form, hideLogin=True)
        case False:
            return redirect(direct)
