from helpers import (
    ssl,
    abort,
    flash,
    smtplib,
    randint,
    sqlite3,
    request,
    session,
    redirect,
    Blueprint,
    RECAPTCHA,
    EmailMessage,
    requestsPost,
    DB_USERS_ROOT,
    verifyUserForm,
    render_template,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_VERIFY_USER,
    message as messageDebugging,
)

verifyUserBlueprint = Blueprint("verifyUser", __name__)


@verifyUserBlueprint.route("/verifyUser/codesent=<codeSent>", methods=["GET", "POST"])
def verifyUser(codeSent):
    match "userName" in session:
        case True:
            userName = session["userName"]
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select isVerified from users where lower(username) = ? """,
                [(userName.lower())],
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
                            match request.method == "POST":
                                case True:
                                    code = request.form["code"]
                                    match code == verificationCode:
                                        case True:
                                            match RECAPTCHA and RECAPTCHA_VERIFY_USER:
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
                                                            messageDebugging("2",f"USER VERIFY RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            cursor.execute(
                                                                """update users set isVerified = "True" where lower(userName) = ? """,
                                                                [(userName.lower())],
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
                                                            messageDebugging("1",f"USER VERIFY RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            abort(401)
                                                case False:
                                                    cursor.execute(
                                                        """update users set isVerified = "True" where lower(userName) = ? """,
                                                        [(userName.lower())],
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
                                "verifyUser.html",
                                form=form,
                                mailSent=True,
                                siteKey=RECAPTCHA_SITE_KEY,
                                recaptcha=RECAPTCHA,
                            )
                        case "false":
                            match request.method == "POST":
                                case True:
                                    connection = sqlite3.connect(DB_USERS_ROOT)
                                    cursor = connection.cursor()
                                    cursor.execute(
                                        """select * from users where lower(userName) = ? """,
                                        [(userName.lower())],
                                    )
                                    userNameDB = cursor.fetchone()
                                    cursor.execute(
                                        """select email from users where lower(username) = ? """,
                                        [(userName.lower())],
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
                                            match RECAPTCHA and RECAPTCHA_VERIFY_USER:
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
                                                            messageDebugging("2",f"USER VERIFY RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            server.send_message(message)
                                                        case False:
                                                            messageDebugging("1",f"USER VERIFY RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                            abort(401)
                                                case False:
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
                                "verifyUser.html", form=form, mailSent=False, siteKey=RECAPTCHA_SITE_KEY, recaptcha=RECAPTCHA,
                            )
        case False:
            return redirect("/")
