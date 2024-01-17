from helpers import (
    flash,
    session,
    sqlite3,
    request,
    message,
    redirect,
    addPoints,
    Blueprint,
    signUpForm,
    currentDate,
    currentTime,
    sha256_crypt,
    DB_USERS_ROOT,
    render_template,
)
from constants import REGISTRATION

signUpBlueprint = Blueprint("signup", __name__)


@signUpBlueprint.route("/signup", methods=["GET", "POST"])
def signup():
    match REGISTRATION:
        case True:
            match "userName" in session:
                case True:
                    message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
                    return redirect("/")
                case False:
                    form = signUpForm(request.form)
                    match request.method == "POST":
                        case True:
                            userName = request.form["userName"]
                            email = request.form["email"]
                            password = request.form["password"]
                            passwordConfirm = request.form["passwordConfirm"]
                            userName = userName.replace(" ", "")
                            connection = sqlite3.connect(DB_USERS_ROOT)
                            cursor = connection.cursor()
                            cursor.execute("select userName from users")
                            users = str(cursor.fetchall())
                            cursor.execute("select email from users")
                            mails = str(cursor.fetchall())
                            match not userName in users and not email in mails:
                                case True:
                                    match passwordConfirm == password:
                                        case True:
                                            match userName.isascii():
                                                case True:
                                                    password = sha256_crypt.hash(
                                                        password
                                                    )
                                                    connection = sqlite3.connect(
                                                        DB_USERS_ROOT
                                                    )
                                                    cursor = connection.cursor()
                                                    cursor.execute(
                                                        f"""
                                                        insert into users(userName,email,password,profilePicture,role,points,creationDate,creationTime,isVerified) \
                                                        values(?, ?, ?, ?, ?, ?, ?, ?, ?)
                                                        """,
                                                        (
                                                            userName,
                                                            email,
                                                            password,
                                                            f"https://api.dicebear.com/7.x/identicon/svg?seed={userName}&radius=10",
                                                            "user",
                                                            0,
                                                            currentDate(),
                                                            currentTime(),
                                                            "False",
                                                        ),
                                                    )
                                                    connection.commit()
                                                    message(
                                                        "2",
                                                        f'USER: "{userName}" ADDED TO DATABASE',
                                                    )
                                                    session["userName"] = userName
                                                    addPoints(1, session["userName"])
                                                    message(
                                                        "2",
                                                        f'USER: "{userName}" LOGGED IN',
                                                    )
                                                    flash(
                                                        f"Welcome {userName}", "success"
                                                    )
                                                    return redirect(
                                                        "/verifyUser/codesent=false"
                                                    )
                                                case False:
                                                    message(
                                                        "1",
                                                        f'USERNAME: "{userName}" DOES NOT FITS ASCII CHARACTERS',
                                                    )
                                                    flash(
                                                        "username does not fit ascii charecters",
                                                        "error",
                                                    )
                                        case False:
                                            message("1", " PASSWORDS MUST MATCH ")
                                            flash("password must match", "error")
                            match userName in users and email in mails:
                                case True:
                                    message(
                                        "1", f'"{userName}" & "{email}" IS UNAVAILABLE '
                                    )
                                    flash(
                                        "This username and email is unavailable.",
                                        "error",
                                    )
                            match not userName in users and email in mails:
                                case True:
                                    message(
                                        "1", f'THIS EMAIL "{email}" IS UNAVAILABLE '
                                    )
                                    flash("This email is unavailable.", "error")
                            match userName in users and not email in mails:
                                case True:
                                    message(
                                        "1",
                                        f'THIS USERNAME "{userName}" IS UNAVAILABLE ',
                                    )
                                    flash("This username is unavailable.", "error")
                    return render_template("signup.html", form=form, hideSignUp=True)
        case False:
            return redirect("/")
