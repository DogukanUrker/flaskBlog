# Import necessary modules and functions
from modules import (
    Log,  # Custom logging module
    ssl,  # SSL/TLS support module
    flash,  # Flash messaging module
    abort,  # Function to abort request processing
    smtplib,  # SMTP protocol client module
    randint,  # Function to generate random integers
    sqlite3,  # SQLite database module
    request,  # Request handling module
    redirect,  # Redirect function
    APP_NAME,  # Application name
    Blueprint,  # Blueprint for defining routes
    SMTP_PORT,  # SMTP server port
    SMTP_MAIL,  # SMTP server email
    RECAPTCHA,  # Flag for enabling reCAPTCHA
    encryption,  # Encryption utility module
    SMTP_SERVER,  # SMTP server address
    EmailMessage,  # Class for creating email messages
    requestsPost,  # Function for making POST requests
    SMTP_PASSWORD,  # SMTP server password
    DB_USERS_ROOT,  # Path to the users database
    render_template,  # Template rendering function
    PasswordResetForm,  # Form class for password reset
    RECAPTCHA_SITE_KEY,  # reCAPTCHA site key
    RECAPTCHA_VERIFY_URL,  # reCAPTCHA verification URL
    RECAPTCHA_SECRET_KEY,  # reCAPTCHA secret key
    RECAPTCHA_PASSWORD_RESET,  # Flag for enabling reCAPTCHA for password reset
)

# Create a blueprint for the password reset route
passwordResetBlueprint = Blueprint("passwordReset", __name__)


# Define a route for password reset
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
    # Define global variables
    global userName
    global passwordResetCode

    # Initialize password reset form
    form = PasswordResetForm(request.form)

    # Check if code has been sent
    match codeSent:
        case "true":
            Log.sql(
                f"Connecting to '{DB_USERS_ROOT}' database"
            )  # Log the database connection is started
            # Code has been sent, handle form submission
            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = connection.cursor()
            match request.method == "POST":
                case True:
                    # Retrieve form data
                    code = request.form["code"]
                    password = request.form["password"]
                    passwordConfirm = request.form["passwordConfirm"]
                    match code == passwordResetCode:
                        case True:
                            # Check if passwords match
                            cursor.execute(
                                """select password from users where lower(userName) = ? """,
                                [(userName.lower())],
                            )
                            oldPassword = cursor.fetchone()[0]
                            match password == passwordConfirm:
                                case True:
                                    # Check if new password is different from old password
                                    match encryption.verify(password, oldPassword):
                                        case True:
                                            flash(
                                                "New password cannot be the same as the old password.",
                                                "error",
                                            )
                                        case False:
                                            # Hash new password and update in the database
                                            password = encryption.hash(password)
                                            match RECAPTCHA and RECAPTCHA_PASSWORD_RESET:
                                                case True:
                                                    # Perform reCAPTCHA verification
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
                                                            # Successful reCAPTCHA verification, update password
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
                                                            flash(
                                                                "You need to login with the new password.",
                                                                "success",
                                                            )
                                                            return redirect(
                                                                "/login/redirect=&"
                                                            )
                                                        case False:
                                                            # Failed reCAPTCHA verification
                                                            Log.danger(
                                                                f"Password reset reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)
                                                case False:
                                                    # No reCAPTCHA, update password
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
                                                    flash(
                                                        "You need to login with the new password.",
                                                        "success",
                                                    )
                                                    return redirect("/login/redirect=&")
                                case False:
                                    # Passwords don't match
                                    flash("Passwords must match.", "error")
                        case False:
                            # Incorrect code entered
                            flash("Wrong code.", "error")
            # Render password reset template with appropriate form and messages
            return render_template(
                "passwordReset.html.jinja",
                form=form,
                mailSent=True,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
        case "false":
            # Code has not been sent, handle form submission
            match request.method == "POST":
                case True:
                    # Retrieve form data
                    userName = request.form["userName"]
                    email = request.form["email"]
                    userName = userName.replace(" ", "")
                    Log.sql(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
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
                            # User and email found, send password reset code
                            context = ssl.create_default_context()
                            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                            server.ehlo()
                            server.starttls(context=context)
                            server.ehlo()
                            server.login(SMTP_MAIL, SMTP_PASSWORD)
                            passwordResetCode = str(randint(1000, 9999))
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
                                    # Perform reCAPTCHA verification
                                    secretResponse = request.form[
                                        "g-recaptcha-response"
                                    ]
                                    verifyResponse = requestsPost(
                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                    ).json()
                                    match verifyResponse[
                                        "success"
                                    ] == True or verifyResponse["score"] > 0.5:
                                        case True:
                                            # Successful reCAPTCHA verification, send email
                                            Log.success(
                                                f"Password reset reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            server.send_message(message)
                                        case False:
                                            # Failed reCAPTCHA verification
                                            Log.danger(
                                                f"Password reset reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                            )
                                            abort(401)
                                case False:
                                    # No reCAPTCHA, send email
                                    server.send_message(message)
                            server.quit()
                            Log.success(
                                f'Password reset code: "{passwordResetCode}" sent to "{email}"',
                            )
                            flash("Code sent.", "success")
                            return redirect("/passwordreset/codesent=true")
                        case True:
                            # User or email not found
                            Log.danger(f'User: "{userName}" not found')
                            flash("User not found.", "error")
            # Render password reset template with appropriate form and messages
            return render_template(
                "passwordReset.html.jinja",
                form=form,
                mailSent=False,
                siteKey=RECAPTCHA_SITE_KEY,
                recaptcha=RECAPTCHA,
            )
