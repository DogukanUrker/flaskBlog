from helpers import (
    session,
    secrets,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    signUpForm,
    sha256_crypt,
)

signUpBlueprint = Blueprint("signup", __name__)


@signUpBlueprint.route("/signup", methods=["GET", "POST"])
def signup():
    match "userName" in session:
        case True:
            message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
            return redirect("/")
        case False:
            form = signUpForm(request.form)
            if request.method == "POST":
                userName = request.form["userName"]
                email = request.form["email"]
                password = request.form["password"]
                passwordConfirm = request.form["passwordConfirm"]
                userName = userName.replace(" ", "")
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute("select userName from users")
                users = str(cursor.fetchall())
                cursor.execute("select email from users")
                mails = str(cursor.fetchall())
                if not userName in users and not email in mails:
                    if passwordConfirm == password:
                        match userName.isascii():
                            case True:
                                password = sha256_crypt.hash(password)
                                connection = sqlite3.connect("db/users.db")
                                cursor = connection.cursor()
                                cursor.execute(
                                    f"""
                                    insert into users(userName,email,password,profilePicture,role,points,creationDate,creationTime) 
                                    values("{userName}","{email}","{password}",
                                    "https://api.dicebear.com/5.x/identicon/svg?seed={secrets.token_urlsafe(32)}",
                                    "user",0,
                                    "{currentDate()}",
                                    "{currentTime()}")
                                    """
                                )
                                connection.commit()
                                message("2", f'USER: "{userName}" ADDED TO DATABASE')
                                return redirect("/")
                            case False:
                                message(
                                    "1",
                                    f'USERNAME: "{userName}" DOES NOT FITS ASCII CHARACTERS',
                                )
                                flash("username does not fit ascii charecters", "error")
                    elif passwordConfirm != password:
                        message("1", " PASSWORDS MUST MATCH ")
                        flash("password must match", "error")
                elif userName in users and email in mails:
                    message("1", f'"{userName}" & "{email}" IS UNAVAILABLE ')
                    flash("This username and email is unavailable.", "error")
                elif not userName in users and email in mails:
                    message("1", f'THIS EMAIL "{email}" IS UNAVAILABLE ')
                    flash("This email is unavailable.", "error")
                elif userName in users and not email in mails:
                    message("1", f'THIS USERNAME "{userName}" IS UNAVAILABLE ')
                    flash("This username is unavailable.", "error")
            return render_template("signup.html", form=form, hideSignUp=True)
