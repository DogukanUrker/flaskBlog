import smtplib
import sqlite3
import ssl
from email.message import EmailMessage

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
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SIGN_UP,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    REGISTRATION,
    SMTP_MAIL,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_SERVER,
)
from utils.addPoints import addPoints
from utils.flashMessage import flashMessage
from utils.forms.SignUpForm import SignUpForm
from utils.log import Log
from utils.time import currentTimeStamp

signUpBlueprint = Blueprint("signup", __name__)


@signUpBlueprint.route("/signup", methods=["GET", "POST"])
def signup():
    """
    This function handles the sign up route.

    If the user is already signed in, they will be redirected to the homepage.
    If the user submits the sign up form, their information is checked to ensure it is valid.
    If the information is valid, their account is created and they are signed in.

    Returns:
    The sign up page with any errors or a confirmation message.
    """

    if REGISTRATION:
        if "userName" in session:
            Log.error(f'USER: "{session["userName"]}" ALREADY LOGGED IN')
            return redirect("/")
        else:
            form = SignUpForm(request.form)

            if request.method == "POST":
                userName = request.form["userName"]
                email = request.form["email"]
                password = request.form["password"]
                passwordConfirm = request.form["passwordConfirm"]

                userName = userName.replace(" ", "")
                Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

                connection = sqlite3.connect(DB_USERS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()

                cursor.execute("select userName from users")
                users = str(cursor.fetchall())
                cursor.execute("select email from users")
                mails = str(cursor.fetchall())

                if userName not in users and email not in mails:
                    if passwordConfirm == password:
                        if userName.isascii():
                            password = encryption.hash(password)

                            connection = sqlite3.connect(DB_USERS_ROOT)
                            connection.set_trace_callback(Log.database)

                            if RECAPTCHA and RECAPTCHA_SIGN_UP:
                                secretResponse = request.form["g-recaptcha-response"]
                                verifyResponse = requestsPost(
                                    url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                ).json()

                                if (
                                    verifyResponse["success"] is True
                                    or verifyResponse["score"] > 0.5
                                ):
                                    Log.success(
                                        f"Sign up reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )

                                    cursor = connection.cursor()
                                    cursor.execute(
                                        """
                                        insert into users(userName,email,password,profilePicture,role,points,timeStamp,isVerified) \
                                        values(?, ?, ?, ?, ?, ?, ?, ?)
                                        """,
                                        (
                                            userName,
                                            email,
                                            password,
                                            f"https://api.dicebear.com/7.x/identicon/svg?seed={userName}&radius=10",
                                            "user",
                                            0,
                                            currentTimeStamp(),
                                            "False",
                                        ),
                                    )
                                    connection.commit()

                                    Log.success(f'User: "{userName}" added to database')

                                    session["userName"] = userName

                                    addPoints(1, session["userName"])

                                    Log.success(f'User: "{userName}" logged in')

                                    flashMessage(
                                        page="signup",
                                        message="success",
                                        category="success",
                                        language=session["language"],
                                    )

                                    context = ssl.create_default_context()
                                    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                                    server.ehlo()
                                    server.starttls(context=context)
                                    server.ehlo()
                                    server.login(SMTP_MAIL, SMTP_PASSWORD)

                                    mail = EmailMessage()
                                    mail.set_content(
                                        f"Hi {userName}👋,\n Welcome to {APP_NAME}"
                                    )
                                    mail.add_alternative(
                                        f"""\
                                    <html>
                                    <body>
                                        <div
                                        style="font-family: Arial, sans-serif;  max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius:0.5rem;"
                                        >
                                        <div style="text-align: center;">
                                            <h1 style="color: #F43F5E;">
                                            Hi {userName}, <br />
                                            Welcome to {APP_NAME}!
                                            </h1>
                                            <p style="font-size: 16px;">
                                            We are glad you joined us.
                                            </p>
                                        </div>
                                        </div>
                                    </body>
                                    </html>
                                    """,
                                        subtype="html",
                                    )
                                    mail["Subject"] = f"Welcome to {APP_NAME}"
                                    mail["From"] = SMTP_MAIL
                                    mail["To"] = email

                                    server.send_message(mail)
                                    server.quit()

                                    return redirect("/verifyUser/codesent=false")
                                else:
                                    Log.error(
                                        f"Sign up reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                    )
                                    abort(401)
                            else:
                                cursor = connection.cursor()
                                cursor.execute(
                                    """
                                            insert into users(userName,email,password,profilePicture,role,points,timeStamp,isVerified) \
                                            values(?, ?, ?, ?, ?, ?, ?, ?)
                                            """,
                                    (
                                        userName,
                                        email,
                                        password,
                                        f"https://api.dicebear.com/7.x/identicon/svg?seed={userName}&radius=10",
                                        "user",
                                        0,
                                        currentTimeStamp(),
                                        "False",
                                    ),
                                )
                                connection.commit()

                                Log.success(f'User: "{userName}" added to databse')

                                session["userName"] = userName

                                addPoints(1, session["userName"])

                                Log.success(f'User: "{userName}" logged in')
                                flashMessage(
                                    page="signup",
                                    message="success",
                                    category="success",
                                    language=session["language"],
                                )

                                context = ssl.create_default_context()
                                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                                server.ehlo()
                                server.starttls(context=context)
                                server.ehlo()
                                server.login(SMTP_MAIL, SMTP_PASSWORD)

                                mail = EmailMessage()
                                mail.set_content(
                                    f"Hi {userName}👋,\n Welcome to {APP_NAME}"
                                )
                                mail.add_alternative(
                                    f"""\
                                    <html>
                                    <body>
                                        <div
                                        style="font-family: Arial, sans-serif;  max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius:0.5rem;"
                                        >
                                        <div style="text-align: center;">
                                            <h1 style="color: #F43F5E;">
                                            Hi {userName}, <br />
                                            Welcome to {APP_NAME}!
                                            </h1>
                                            <p style="font-size: 16px;">
                                            We are glad you joined us.
                                            </p>
                                        </div>
                                        </div>
                                    </body>
                                    </html>
                                """,
                                    subtype="html",
                                )
                                mail["Subject"] = f"Welcome to {APP_NAME}!👋🏻"
                                mail["From"] = SMTP_MAIL
                                mail["To"] = email

                                server.send_message(mail)
                                server.quit()

                                return redirect("/verifyUser/codesent=false")
                        else:
                            Log.error(
                                f'Username: "{userName}" do not fits to ascii characters',
                            )
                            flashMessage(
                                page="signup",
                                message="ascii",
                                category="error",
                                language=session["language"],
                            )
                    else:
                        Log.error("Passwords do not match")

                        flashMessage(
                            page="signup",
                            message="password",
                            category="error",
                            language=session["language"],
                        )

                if userName in users and email in mails:
                    Log.error(f'"{userName}" & "{email}" is unavailable ')
                    flashMessage(
                        page="signup",
                        message="taken",
                        category="error",
                        language=session["language"],
                    )
                if userName not in users and email in mails:
                    Log.error(f'This email "{email}" is unavailable')

                    flashMessage(
                        page="signup",
                        message="email",
                        category="error",
                        language=session["language"],
                    )
                if userName in users and email not in mails:
                    Log.error(f'This username "{userName}" is unavailable')

                    flashMessage(
                        page="signup",
                        message="username",
                        category="error",
                        language=session["language"],
                    )

            return render_template(
                "signup.html.jinja",
                form=form,
                hideSignUp=True,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
    else:
        return redirect("/")
