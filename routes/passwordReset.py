from helpers import (
    ssl,
    flash,
    smtplib,
    randint,
    sqlite3,
    request,
    redirect,
    Blueprint,
    EmailMessage,
    sha256_crypt,
    render_template,
    passwordResetForm,
    message as messageDebugging,
)

passwordResetBlueprint = Blueprint("passwordReset", __name__)


@passwordResetBlueprint.route(
    "/passwordreset/codesent=<codeSent>", methods=["GET", "POST"]
)
def passwordReset(codeSent):
    global userName
    global passwordResetCode
    form = passwordResetForm(request.form)
    match codeSent:
        case "true":
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            if request.method == "POST":
                code = request.form["code"]
                password = request.form["password"]
                passwordConfirm = request.form["passwordConfirm"]
                match code == passwordResetCode:
                    case True:
                        cursor.execute(
                            f'select password from users where lower(userName) = "{userName.lower()}"'
                        )
                        oldPassword = cursor.fetchone()[0]
                        match password == passwordConfirm:
                            case True:
                                match sha256_crypt.verify(password, oldPassword):
                                    case True:
                                        flash(
                                            "new password can not be same with old password",
                                            "error",
                                        )
                                    case False:
                                        password = sha256_crypt.hash(password)
                                        cursor.execute(
                                            f'update users set password = "{password}" where lower(userName) = "{userName.lower()}"'
                                        )
                                        connection.commit()
                                        messageDebugging(
                                            "2",
                                            f'USER: "{userName}" CHANGED HIS PASSWORD',
                                        )
                                        flash(
                                            "you need login with new password",
                                            "success",
                                        )
                                        return redirect("/login/redirect=&")
                            case False:
                                flash("passwords must match", "error")
                    case False:
                        flash("Wrong Code", "error")
            return render_template("passwordReset.html", form=form, mailSent=True)
        case "false":
            if request.method == "POST":
                userName = request.form["userName"]
                email = request.form["email"]
                userName = userName.replace(" ", "")
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'select * from users where lower(userName) = "{userName.lower()}"'
                )
                userNameDB = cursor.fetchone()
                cursor.execute(
                    f'select * from users where lower(email) = "{email.lower()}"'
                )
                emailDB = cursor.fetchone()
                match not userNameDB or not emailDB:
                    case False:
                        port = 587
                        smtp_server = "smtp.gmail.com"
                        context = ssl.create_default_context()
                        server = smtplib.SMTP(smtp_server, port)
                        server.ehlo()
                        server.starttls(context=context)
                        server.ehlo()
                        server.login(
                            "flaskblogdogukanurker@gmail.com", "lsooxsmnsfnhnixy"
                        )
                        passwordResetCode = str(randint(1000, 9999))
                        message = EmailMessage()
                        message.set_content(
                            f"Hi {userName}👋,\nForgot your password😶‍🌫️? No problem👌.\nHere is your password reset code🔢:\n{passwordResetCode}"
                        )
                        message.add_alternative(
                            f"""\
                        <html>
                            <body>
                                <h2>Hi {userName}👋,</h2>
                                <h3>Forgot your password😶‍🌫️? No problem👌.<br>Here is your password reset code🔢:</h3>
                                <h1>{passwordResetCode}</h1>
                                </body>
                        </html>
                        """,
                            subtype="html",
                        )
                        message["Subject"] = "Forgot Password?😕"
                        message["From"] = "flaskblogdogukanurker@gmail.com"
                        message["To"] = email
                        server.send_message(message)
                        server.quit()
                        messageDebugging(
                            "2",
                            f'PASSWORD RESET CODE: "{passwordResetCode}" SENT TO "{email}"',
                        )
                        flash("code sent", "success")
                        return redirect("/passwordreset/codesent=true")
                    case True:
                        messageDebugging("1", f'USER: "{userName}" NOT FOUND')
                        flash("user not found", "error")
            return render_template("passwordReset.html", form=form, mailSent=False)
