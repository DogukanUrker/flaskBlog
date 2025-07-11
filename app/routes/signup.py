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
from settings import Settings
from utils.addPoints import add_points
from utils.flashMessage import flash_message
from utils.forms.SignUpForm import SignUpForm
from utils.log import Log
from utils.time import current_time_stamp

sign_up_blueprint = Blueprint("signup", __name__)


@sign_up_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    """
    This function handles the sign up route.

    If the user is already signed in, they will be redirected to the homepage.
    If the user submits the sign up form, their information is checked to ensure it is valid.
    If the information is valid, their account is created and they are signed in.

    Returns:
    The sign up page with any errors or a confirmation message.
    """

    if Settings.REGISTRATION:
        if "user_name" in session:
            Log.error(f'USER: "{session["user_name"]}" ALREADY LOGGED IN')
            return redirect("/")
        else:
            form = SignUpForm(request.form)

            if request.method == "POST":
                user_name = request.form["user_name"]
                email = request.form["email"]
                password = request.form["password"]
                password_confirm = request.form["password_confirm"]

                user_name = user_name.replace(" ", "")
                Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

                connection = sqlite3.connect(Settings.DB_USERS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()

                cursor.execute("select user_name from users")
                users = str(cursor.fetchall())
                cursor.execute("select email from users")
                mails = str(cursor.fetchall())

                if user_name not in users and email not in mails:
                    if password_confirm == password:
                        if user_name.isascii():
                            password = encryption.hash(password)

                            if Settings.RECAPTCHA:
                                secret_response = request.form["g-recaptcha-response"]
                                verify_response = requestsPost(
                                    url=f"{Settings.RECAPTCHA_VERIFY_URL}?secret={Settings.RECAPTCHA_SECRET_KEY}&response={secret_response}"
                                ).json()
                                if not (
                                    verify_response["success"] is True
                                    or verify_response.get("score", 0) > 0.5
                                ):
                                    Log.error(
                                        f"Signup reCAPTCHA | verification: {verify_response.get('success')} | score: {verify_response.get('score')}",
                                    )
                                    abort(401)

                                Log.success(
                                    f"Signup reCAPTCHA | verification: {verify_response['success']} | score: {verify_response.get('score')}",
                                )

                            # Create user account
                            connection = sqlite3.connect(Settings.DB_USERS_ROOT)
                            connection.set_trace_callback(Log.database)
                            cursor = connection.cursor()
                            cursor.execute(
                                """
                                insert into users(user_name,email,password,profile_picture,role,points,time_stamp,is_verified) \
                                values(?, ?, ?, ?, ?, ?, ?, ?)
                                """,
                                (
                                    user_name,
                                    email,
                                    password,
                                    f"https://api.dicebear.com/7.x/identicon/svg?seed={user_name}&radius=10",
                                    "user",
                                    0,
                                    current_time_stamp(),
                                    "False",
                                ),
                            )
                            connection.commit()

                            Log.success(f'User: "{user_name}" added to database')

                            session["user_name"] = user_name
                            add_points(1, session["user_name"])
                            Log.success(f'User: "{user_name}" logged in')

                            flash_message(
                                page="signup",
                                message="success",
                                category="success",
                                language=session["language"],
                            )

                            # Send welcome email
                            context = ssl.create_default_context()
                            server = smtplib.SMTP(
                                Settings.SMTP_SERVER, Settings.SMTP_PORT
                            )
                            server.ehlo()
                            server.starttls(context=context)
                            server.ehlo()
                            server.login(Settings.SMTP_MAIL, Settings.SMTP_PASSWORD)

                            mail = EmailMessage()
                            mail.set_content(
                                f"Hi {user_name}👋,\n Welcome to {Settings.APP_NAME}"
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
                                    Hi {user_name}, <br />
                                    Welcome to {Settings.APP_NAME}!
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
                            mail["Subject"] = f"Welcome to {Settings.APP_NAME}"
                            mail["From"] = Settings.SMTP_MAIL
                            mail["To"] = email

                            server.send_message(mail)
                            server.quit()

                            return redirect("/verifyUser/codesent=false")
                        else:
                            Log.error(
                                f'Username: "{user_name}" do not fits to ascii characters',
                            )
                            flash_message(
                                page="signup",
                                message="ascii",
                                category="error",
                                language=session["language"],
                            )
                    else:
                        Log.error("Passwords do not match")

                        flash_message(
                            page="signup",
                            message="password",
                            category="error",
                            language=session["language"],
                        )

                if user_name in users and email in mails:
                    Log.error(f'"{user_name}" & "{email}" is unavailable ')
                    flash_message(
                        page="signup",
                        message="taken",
                        category="error",
                        language=session["language"],
                    )
                if user_name not in users and email in mails:
                    Log.error(f'This email "{email}" is unavailable')

                    flash_message(
                        page="signup",
                        message="email",
                        category="error",
                        language=session["language"],
                    )
                if user_name in users and email not in mails:
                    Log.error(f'This username "{user_name}" is unavailable')

                    flash_message(
                        page="signup",
                        message="username",
                        category="error",
                        language=session["language"],
                    )

            return render_template(
                "signup.html",
                form=form,
                hideSignUp=True,
                siteKey=Settings.RECAPTCHA_SITE_KEY,
                recaptcha=Settings.RECAPTCHA,
            )
    else:
        return redirect("/")
