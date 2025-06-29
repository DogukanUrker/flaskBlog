import smtplib
import sqlite3
import ssl
from email.message import EmailMessage
from random import randint

from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    session,
)
from passlib.hash import sha512_crypt as encryption
from requests import post as requestsPost
from settings import (
    APP_NAME,
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_PASSWORD_RESET,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    SMTP_MAIL,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_SERVER,
)
from utils.flashMessage import flashMessage
from utils.forms.PasswordResetForm import PasswordResetForm
from utils.log import Log

passwordResetBlueprint = Blueprint("passwordReset", __name__)


passwordResetCodesStorage = {}


@passwordResetBlueprint.route(
    "/passwordreset/codesent=<codeSent>", methods=["GET", "POST"]
)
def passwordReset(codeSent):
    """
    This function handles the password reset process.

    Args:
        codeSent (str): A string indicating whether the code has been sent or not.

    Returns:
        A rendered template with the appropriate form and messages.

    Raises:
        401: If the reCAPTCHA verification fails.
    """

    form = PasswordResetForm(request.form)

    match codeSent:
        case "true":
            Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()
            match request.method == "POST":
                case True:
                    userName = request.form["userName"]
                    userName = userName.replace(" ", "")
                    code = request.form["code"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]
                    match code == passwordResetCodesStorage.get(userName, ""):
                        case True:
                            cursor.execute(
                                """select password from users where lower(userName) = ? """,
                                [(userName.lower())],
                            )
                            oldPassword = cursor.fetchone()[0]
                            match password == passwordConfirm:
                                case True:
                                    match encryption.verify(password, oldPassword):
                                        case True:
                                            flashMessage(
                                                page="passwordReset",
                                                message="same",
                                                category="error",
                                                language=session["language"],
                                            )
                                        case False:
                                            passwordResetCodesStorage.pop(userName)

                                            password = encryption.hash(password)
                                            match (
                                                RECAPTCHA and RECAPTCHA_PASSWORD_RESET
                                            ):
                                                case True:
                                                    secretResponse = request.form[
                                                        "g-recaptcha-response"
                                                    ]
                                                    verifyResponse = requestsPost(
                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                    ).json()
                                                    match (
                                                        verifyResponse["success"]
                                                        is True
                                                        or verifyResponse["score"] > 0.5
                                                    ):
                                                        case True:
                                                            Log.success(
                                                                f"Password reset reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            cursor.execute(
                                                                """update users set password = ? where lower(userName) = ? """,
                                                                [
                                                                    (password),
                                                                    (userName.lower()),
                                                                ],
                                                            )
                                                            connection.commit()
                                                            Log.success(
                                                                f'User: "{userName}" changed his password',
                                                            )
                                                            flashMessage(
                                                                page="passwordReset",
                                                                message="success",
                                                                category="success",
                                                                language=session[
                                                                    "language"
                                                                ],
                                                            )
                                                            return redirect(
                                                                "/login/redirect=&"
                                                            )
                                                        case False:
                                                            Log.error(
                                                                f"Password reset reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)
                                                case False:
                                                    cursor.execute(
                                                        """update users set password = ? where lower(userName) = ? """,
                                                        [
                                                            (password),
                                                            (userName.lower()),
                                                        ],
                                                    )
                                                    connection.commit()
                                                    Log.success(
                                                        f'User: "{userName}" changed his password',
                                                    )
                                                    flashMessage(
                                                        page="passwordReset",
                                                        message="success",
                                                        category="success",
                                                        language=session["language"],
                                                    )
                                                    return redirect("/login/redirect=&")
                                case False:
                                    flashMessage(
                                        page="passwordReset",
                                        message="match",
                                        category="error",
                                        language=session["language"],
                                    )
                        case False:
                            flashMessage(
                                page="passwordReset",
                                message="wrong",
                                category="error",
                                language=session["language"],
                            )

            return render_template(
                "passwordReset.html.jinja",
                form=form,
                mailSent=True,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case "false":
            match request.method == "POST":
                case True:
                    userName = request.form["userName"]
                    email = request.form["email"]
                    userName = userName.replace(" ", "")
                    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(Log.database)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select * from users where lower(userName) = ? and lower(email) = ? """,
                        [userName.lower(), email.lower()],
                    )
                    userDB = cursor.fetchone()
                    match not userDB:
                        case False:
                            context = ssl.create_default_context()
                            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                            server.ehlo()
                            server.starttls(context=context)
                            server.ehlo()
                            server.login(SMTP_MAIL, SMTP_PASSWORD)
                            passwordResetCode = str(randint(1000, 9999))
                            passwordResetCodesStorage[userName] = passwordResetCode
                            message = EmailMessage()
                            message.set_content(
                                f"Hi {userName}👋,\nForgot your password😶‍🌫️? No problem👌.\nHere is your password reset code🔢:\n{passwordResetCode}"
                            )
                            message.add_alternative(
                                f"""\
                                <html>
                                <body style="font-family: Arial, sans-serif;">
                                <div style="max-width: 600px;margin: 0 auto;background-color: #ffffff;padding: 20px; border-radius:0.5rem;">
                                    <div style="text-align: center;">
                                    <h1 style="color: #F43F5E;">Password Reset</h1>
                                    <p>Hello, {userName}.</p>
                                    <p>We received a request to reset your password for your account. If you did not request this, please ignore this email.</p>
                                    <p>To reset your password, enter the following code in the app:</p>
                                    <span style="display: inline-block; background-color: #e0e0e0; color: #000000;padding: 10px 20px;font-size: 24px;font-weight: bold; border-radius: 0.5rem;">{passwordResetCode}</span>
                                    <p style="font-family: Arial, sans-serif; font-size: 16px;">This code will expire when you refresh the page.</p>
                                    <p>Thank you for using {APP_NAME}.</p>
                                    </div>
                                </div>
                                </body>
                                </html>
                            """,
                                subtype="html",
                            )
                            message["Subject"] = "Forget Password?🔒"
                            message["From"] = SMTP_MAIL
                            message["To"] = email
                            match RECAPTCHA and RECAPTCHA_PASSWORD_RESET:
                                case True:
                                    secretResponse = request.form[
                                        "g-recaptcha-response"
                                    ]
                                    verifyResponse = requestsPost(
                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                    ).json()
                                    match (
                                        verifyResponse["success"] is True
                                        or verifyResponse["score"] > 0.5
                                    ):
                                        case True:
                                            Log.success(
                                                f"Password reset reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            server.send_message(message)
                                        case False:
                                            Log.error(
                                                f"Password reset reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            abort(401)
                                case False:
                                    server.send_message(message)
                            server.quit()
                            Log.success(
                                f'Password reset code: "{passwordResetCode}" sent to "{email}"',
                            )
                            flashMessage(
                                page="passwordReset",
                                message="code",
                                category="success",
                                language=session["language"],
                            )
                            return redirect("/passwordreset/codesent=true")
                        case True:
                            Log.error(f'User: "{userName}" not found')
                            flashMessage(
                                page="passwordReset",
                                message="notFound",
                                category="error",
                                language=session["language"],
                            )

            return render_template(
                "passwordReset.html.jinja",
                form=form,
                mailSent=False,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
