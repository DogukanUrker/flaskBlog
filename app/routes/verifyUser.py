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
from requests import post as requestsPost
from settings import (
    APP_NAME,
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_VERIFY_USER,
    SMTP_MAIL,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_SERVER,
)
from utils.flashMessage import flashMessage
from utils.forms.VerifyUserForm import VerifyUserForm
from utils.log import Log

verifyUserBlueprint = Blueprint("verifyUser", __name__)


@verifyUserBlueprint.route("/verifyUser/codesent=<codeSent>", methods=["GET", "POST"])
def verifyUser(codeSent):
    """
    This function handles the verification of the user's account.

    Args:
        codeSent (str): A string indicating whether the verification code has been sent or not.

    Returns:
        redirect: A redirect to the homepage if the user is verified, or a rendered template with the verification form.

    """

    match "userName" in session:
        case True:
            userName = session["userName"]
            Log.database(f"Connecting to '{DB_USERS_ROOT}' database")
            Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(Log.database)
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

                    form = VerifyUserForm(request.form)

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

                                                    match (
                                                        verifyResponse["success"]
                                                        is True
                                                        or verifyResponse["score"] > 0.5
                                                    ):
                                                        case True:
                                                            Log.success(
                                                                f"User verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )

                                                            cursor.execute(
                                                                """update users set isVerified = "True" where lower(userName) = ? """,
                                                                [(userName.lower())],
                                                            )
                                                            connection.commit()
                                                            Log.success(
                                                                f'User: "{userName}" has been verified'
                                                            )
                                                            flashMessage(
                                                                page="verifyUser",
                                                                message="success",
                                                                category="success",
                                                                language=session[
                                                                    "language"
                                                                ],
                                                            )
                                                            return redirect("/")
                                                        case False:
                                                            Log.error(
                                                                f"User Verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)
                                                case False:
                                                    cursor.execute(
                                                        """update users set isVerified = "True" where lower(userName) = ? """,
                                                        [(userName.lower())],
                                                    )
                                                    connection.commit()
                                                    Log.success(
                                                        f'User: "{userName}" has been verified'
                                                    )
                                                    flashMessage(
                                                        page="verifyUser",
                                                        message="success",
                                                        category="success",
                                                        language=session["language"],
                                                    )
                                                    return redirect("/")
                                        case False:
                                            flashMessage(
                                                page="verifyUser",
                                                message="wrong",
                                                category="error",
                                                language=session["language"],
                                            )

                            return render_template(
                                "verifyUser.html.jinja",
                                form=form,
                                mailSent=True,
                                siteKey=RECAPTCHA_SITE_KEY,
                                recaptcha=RECAPTCHA,
                            )
                        case "false":
                            match request.method == "POST":
                                case True:
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
                                            context = ssl.create_default_context()
                                            server = smtplib.SMTP(
                                                SMTP_SERVER, SMTP_PORT
                                            )
                                            server.ehlo()
                                            server.starttls(context=context)
                                            server.ehlo()
                                            server.login(
                                                SMTP_MAIL,
                                                SMTP_PASSWORD,
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
                                                        <div
                                                        style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius:0.5rem;"
                                                        >
                                                        <div style="text-align: center;">
                                                            <h1 style="color: #F43F5E;">Thank you for creating an account!</h1>
                                                            <p style="font-size: 16px;">
                                                            Hello, {userName}.
                                                            </p>
                                                            <p style="font-size: 16px;">
                                                            We are glad you joined us at {APP_NAME}. You can now enjoy our amazing
                                                            features and services.
                                                            </p>
                                                            <p style="font-size: 16px;">
                                                            To verify your email address, enter the following code in the app:
                                                            </p>
                                                            <span
                                                            style="display: inline-block; background-color: #e0e0e0; color: #000000; padding: 10px 20px; font-size: 24px; font-weight: bold; border-radius: 0.5rem;"
                                                            >{verificationCode}</span
                                                            >
                                                            <p style="font-size: 16px;">
                                                            This code will expire when you refresh the page.
                                                            </p>
                                                            <p style="font-size: 16px;">
                                                            Thank you for choosing {APP_NAME}.
                                                            </p>
                                                        </div>
                                                        </div>
                                                    </body>
                                                    </html>
                                            """,
                                                subtype="html",
                                            )
                                            message["Subject"] = "Verification Code🔢"
                                            message["From"] = SMTP_MAIL
                                            message["To"] = email

                                            match RECAPTCHA and RECAPTCHA_VERIFY_USER:
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
                                                                f"User verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            server.send_message(message)
                                                        case False:
                                                            Log.error(
                                                                f"User verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)
                                                case False:
                                                    server.send_message(message)

                                            server.quit()
                                            Log.success(
                                                f'Verification code: "{verificationCode}" sent to "{email[0]}"',
                                            )
                                            flashMessage(
                                                page="verifyUser",
                                                message="code",
                                                category="success",
                                                language=session["language"],
                                            )
                                            return redirect("/verifyUser/codesent=true")
                                        case True:
                                            Log.error(f'User: "{userName}" not found')
                                            flashMessage(
                                                page="verifyUser",
                                                message="notFound",
                                                category="error",
                                                language=session["language"],
                                            )

                            return render_template(
                                "verifyUser.html.jinja",
                                form=form,
                                mailSent=False,
                                siteKey=RECAPTCHA_SITE_KEY,
                                recaptcha=RECAPTCHA,
                            )
        case False:
            Log.error(
                f"{request.remote_addr} tried to verify his account without being logged in"
            )
            return redirect("/")
