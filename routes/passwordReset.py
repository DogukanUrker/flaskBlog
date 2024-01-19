from helpers import (
    ssl,
    flash,
    abort,
    smtplib,
    randint,
    sqlite3,
    request,
    redirect,
    Blueprint,
    EmailMessage,
    sha256_crypt,
    RECAPTCHA,
    requestsPost,
    DB_USERS_ROOT,
    render_template,
    passwordResetForm,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_PASSWORD_RESET,
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
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            match request.method == "POST":
                case True:
                    code = request.form["code"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]
                    match code == passwordResetCode:
                        case True:
                            cursor.execute(
                                """select password from users where lower(userName) = ? """,
                                [(userName.lower())],
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
                                            match RECAPTCHA and RECAPTCHA_PASSWORD_RESET:
                                                case True:
                                                    secretResponse = request.form[
                                                                        "g-recaptcha-response"
                                                                    ]
                                                    verifyResponse = requestsPost(
                                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                                    ).json()
                                                    match verifyResponse[
                                                                        "success"
                                                                    ] == True or verifyResponse[
                                                                        "score"
                                                                    ] > 0.5:
                                                        case True:
                                                            messageDebugging("2",f"PASSWORD RESET RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            cursor.execute(
                                                                """update users set password = ? where lower(userName) = ? """,
                                                                [(password), (userName.lower())],
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
                                                            messageDebugging("1",f"PASSWORD RESET RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            abort(401)
                                                case False:
                                                    cursor.execute(
                                                        """update users set password = ? where lower(userName) = ? """,
                                                        [(password), (userName.lower())],
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
            return render_template("passwordReset.html", form=form, mailSent=True, siteKey=RECAPTCHA_SITE_KEY, recaptcha=RECAPTCHA,)
        case "false":
            match request.method == "POST":
                case True:
                    userName = request.form["userName"]
                    email = request.form["email"]
                    userName = userName.replace(" ", "")
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select * from users where lower(userName) = ? """,
                        [(userName.lower())],
                    )
                    userNameDB = cursor.fetchone()
                    cursor.execute(
                        """select * from users where lower(email) = ? """,
                        [(email.lower())],
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
                            match RECAPTCHA and RECAPTCHA_PASSWORD_RESET:
                                case True:
                                    secretResponse = request.form[
                                                        "g-recaptcha-response"
                                                    ]
                                    verifyResponse = requestsPost(
                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                    ).json()
                                    match verifyResponse[
                                                        "success"
                                                    ] == True or verifyResponse[
                                                        "score"
                                                    ] > 0.5:
                                        case True:
                                            messageDebugging("2",f"PASSWORD RESET RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                            server.send_message(message)
                                        case False:
                                            messageDebugging("1",f"PASSWORD RESET RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                            abort(401)
                                case False:
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
            return render_template("passwordReset.html", form=form, mailSent=False, siteKey=RECAPTCHA_SITE_KEY, recaptcha=RECAPTCHA,)
