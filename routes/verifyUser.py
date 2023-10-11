from helpers import (
    ssl,
    flash,
    smtplib,
    randint,
    sqlite3,
    request,
    session,
    redirect,
    Blueprint,
    EmailMessage,
    render_template,
    verifyUserForm,
    message as messageDebugging,
)

verifyUserBlueprint = Blueprint("verifyUser", __name__)


@verifyUserBlueprint.route("/verifyUser/codesent=<codeSent>", methods=["GET", "POST"])
def verifyUser(codeSent):
    match "userName" in session:
        case True:
            userName = session["userName"]
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select isVerified from users where lower(username) = "{userName.lower()}"'
            )
            isVerfied = cursor.fetchone()[0]
            match isVerfied:
                case "True":
                    return redirect("/")
                case "False":
                    global verificationCode
                    form = verifyUserForm(request.form)
                    match codeSent:
                        case "true":
                            if request.method == "POST":
                                code = request.form["code"]
                                match code == verificationCode:
                                    case True:
                                        cursor.execute(
                                            f'update users set isVerified = "True" where lower(userName) = "{userName.lower()}"'
                                        )
                                        connection.commit()
                                        messageDebugging(
                                            "2",
                                            f'USER: "{userName}" HAS BEEN VERIFIED',
                                        )
                                        flash(
                                            "Your account has been verified.",
                                            "success",
                                        )
                                        return redirect("/")
                                    case False:
                                        flash("Wrong Code", "error")
                            return render_template(
                                "verifyUser.html", form=form, mailSent=True
                            )
                        case "false":
                            if request.method == "POST":
                                connection = sqlite3.connect("db/users.db")
                                cursor = connection.cursor()
                                cursor.execute(
                                    f'select * from users where lower(userName) = "{userName.lower()}"'
                                )
                                userNameDB = cursor.fetchone()
                                cursor.execute(
                                    f'select email from users where lower(username) = "{userName.lower()}"'
                                )
                                email = cursor.fetchone()
                                match not userNameDB:
                                    case False:
                                        port = 587
                                        smtp_server = "smtp.gmail.com"
                                        context = ssl.create_default_context()
                                        server = smtplib.SMTP(smtp_server, port)
                                        server.ehlo()
                                        server.starttls(context=context)
                                        server.ehlo()
                                        server.login(
                                            "flaskblogdogukanurker@gmail.com",
                                            "lsooxsmnsfnhnixy",
                                        )
                                        verificationCode = str(randint(1000, 9999))
                                        message = EmailMessage()
                                        message.set_content(
                                            f"Hi {userName}👋,\nHere is your account verification code🔢:\n{verificationCode}"
                                        )
                                        message.add_alternative(
                                            f"""\
                                        <html>
                                            <body>
                                                <h2>Hi {userName}👋,</h2>
                                                <h3>Here is your account verification code🔢:</h3>
                                                <h1>{verificationCode}</h1>
                                                </body>
                                        </html>
                                        """,
                                            subtype="html",
                                        )
                                        message["Subject"] = "Verification Code🔢"
                                        message[
                                            "From"
                                        ] = "flaskblogdogukanurker@gmail.com"
                                        message["To"] = email
                                        server.send_message(message)
                                        server.quit()
                                        messageDebugging(
                                            "2",
                                            f'VERIFICATION CODE: "{verificationCode}" SENT TO "{email}"',
                                        )
                                        flash("code sent", "success")
                                        return redirect("/verifyUser/codesent=true")
                                    case True:
                                        messageDebugging(
                                            "1", f'USER: "{userName}" NOT FOUND'
                                        )
                                        flash("user not found", "error")
                            return render_template(
                                "verifyUser.html", form=form, mailSent=False
                            )
        case False:
            return redirect("/")
