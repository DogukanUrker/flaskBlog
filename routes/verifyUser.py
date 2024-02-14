# Import necessary modules and functions
from modules import (
    Log,  # Logging module
    ssl,  # SSL/TLS module
    abort,  # Function for aborting requests
    flash,  # Flash messaging module
    smtplib,  # SMTP client module
    randint,  # Function for generating random integers
    sqlite3,  # SQLite database module
    request,  # Module for handling HTTP requests
    session,  # Session management module
    redirect,  # Function for redirecting requests
    APP_NAME,  # Constant for application name
    Blueprint,  # Blueprint class for creating modular applications
    SMTP_PORT,  # SMTP port number
    SMTP_MAIL,  # SMTP email address
    RECAPTCHA,  # Recaptcha module
    SMTP_SERVER,  # SMTP server address
    EmailMessage,  # Class for creating email messages
    requestsPost,  # Module for making HTTP POST requests
    SMTP_PASSWORD,  # SMTP password
    DB_USERS_ROOT,  # Path to the users database
    VerifyUserForm,  # Form for verifying user
    render_template,  # Function for rendering templates
    RECAPTCHA_SITE_KEY,  # Recaptcha site key
    RECAPTCHA_VERIFY_URL,  # Recaptcha verification URL
    RECAPTCHA_SECRET_KEY,  # Recaptcha secret key
    RECAPTCHA_VERIFY_USER,  # Flag for enabling/disabling Recaptcha for verify user
)

# Create a blueprint for the verify user route
verifyUserBlueprint = Blueprint("verifyUser", __name__)


# Define a route for verifying user
@verifyUserBlueprint.route("/verifyUser/codesent=<codeSent>", methods=["GET", "POST"])
def verifyUser(codeSent):
    """
    This function handles the verification of the user's account.

    Args:
        codeSent (str): A string indicating whether the verification code has been sent or not.

    Returns:
        redirect: A redirect to the homepage if the user is verified, or a rendered template with the verification form.

    """
    # Check if "userName" exists in session
    match "userName" in session:
        case True:
            # Get the username from session
            userName = session["userName"]
            Log.sql(
                f"Connecting to '{DB_USERS_ROOT}' database"
            )  # Log the database connection is started
            Log.sql(
                f"Connecting to '{DB_USERS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the users database
            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = connection.cursor()
            # Check if the user is already verified
            cursor.execute(
                """select isVerified from users where lower(username) = ? """,
                [(userName.lower())],
            )
            isVerfied = cursor.fetchone()[0]
            # Check if the user is already verified
            match isVerfied:
                case "True":
                    return redirect(
                        "/"
                    )  # Redirect to homepage if user is already verified
                case "False":
                    global verificationCode  # Declare a global variable for verification code
                    # Create verification form instance
                    form = VerifyUserForm(request.form)
                    # Check if code has been sent
                    match codeSent:
                        case "true":
                            # Check if request method is POST
                            match request.method == "POST":
                                case True:
                                    # Retrieve verification code from the form
                                    code = request.form["code"]
                                    # Check if the entered code matches the verification code
                                    match code == verificationCode:
                                        case True:
                                            # Check Recaptcha if enabled
                                            match RECAPTCHA and RECAPTCHA_VERIFY_USER:
                                                case True:
                                                    # Verify Recaptcha response
                                                    secretResponse = request.form[
                                                        "g-recaptcha-response"
                                                    ]
                                                    verifyResponse = requestsPost(
                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                    ).json()
                                                    # Check Recaptcha verification result
                                                    match verifyResponse[
                                                        "success"
                                                    ] == True or verifyResponse[
                                                        "score"
                                                    ] > 0.5:
                                                        case True:
                                                            # Recaptcha verification successful
                                                            Log.success(
                                                                f"User verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            # Update user's verification status in the database
                                                            cursor.execute(
                                                                """update users set isVerified = "True" where lower(userName) = ? """,
                                                                [(userName.lower())],
                                                            )
                                                            connection.commit()
                                                            Log.success(
                                                                f'User: "{userName}" has been verified'
                                                            )
                                                            flash(
                                                                "Your account has been verified.",
                                                                "success",
                                                            )
                                                            return redirect("/")
                                                        case False:
                                                            # Recaptcha verification failed
                                                            Log.danger(
                                                                f"User Verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)
                                                case False:
                                                    # Recaptcha not enabled
                                                    cursor.execute(
                                                        """update users set isVerified = "True" where lower(userName) = ? """,
                                                        [(userName.lower())],
                                                    )
                                                    connection.commit()
                                                    Log.success(
                                                        f'User: "{userName}" has been verified'
                                                    )
                                                    flash(
                                                        "Your account has been verified.",
                                                        "success",
                                                    )
                                                    return redirect("/")
                                        case False:
                                            # Wrong verification code entered
                                            flash("Wrong code.", "error")
                            # Render the verification form template
                            return render_template(
                                "verifyUser.html.jinja",
                                form=form,
                                mailSent=True,
                                siteKey=RECAPTCHA_SITE_KEY,
                                recaptcha=RECAPTCHA,
                            )
                        case "false":
                            # Check if request method is POST
                            match request.method == "POST":
                                case True:
                                    # Check if user exists in the database
                                    cursor.execute(
                                        """select * from users where lower(userName) = ? """,
                                        [(userName.lower())],
                                    )
                                    userNameDB = cursor.fetchone()
                                    # Get user's email from the database
                                    cursor.execute(
                                        """select email from users where lower(username) = ? """,
                                        [(userName.lower())],
                                    )
                                    email = cursor.fetchone()
                                    # Check if user exists in the database
                                    match not userNameDB:
                                        case False:
                                            # Connect to SMTP server and send verification code via email
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
                                            # Generate a random verification code
                                            verificationCode = str(randint(1000, 9999))
                                            # Create an email message with the verification code
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
                                            # Check Recaptcha if enabled
                                            match RECAPTCHA and RECAPTCHA_VERIFY_USER:
                                                case True:
                                                    # Verify Recaptcha response
                                                    secretResponse = request.form[
                                                        "g-recaptcha-response"
                                                    ]
                                                    verifyResponse = requestsPost(
                                                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                    ).json()
                                                    # Check Recaptcha verification result
                                                    match verifyResponse[
                                                        "success"
                                                    ] == True or verifyResponse[
                                                        "score"
                                                    ] > 0.5:
                                                        case True:
                                                            # Recaptcha verification successful, send verification email
                                                            Log.success(
                                                                f"User verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            server.send_message(message)
                                                        case False:
                                                            # Recaptcha verification failed
                                                            Log.danger(
                                                                f"User verify reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                                                            )
                                                            abort(401)
                                                case False:
                                                    # Recaptcha not enabled, send verification email
                                                    server.send_message(message)
                                            # Close connection to SMTP server
                                            server.quit()
                                            Log.success(
                                                f'Verification code: "{verificationCode}" sent to "{email[0]}"',
                                            )
                                            flash("Code sent.", "success")
                                            return redirect("/verifyUser/codesent=true")
                                        case True:
                                            # User not found in the database
                                            Log.danger(f'User: "{userName}" not found')
                                            flash("User not found.", "error")
                            # Render the verification form template
                            return render_template(
                                "verifyUser.html.jinja",
                                form=form,
                                mailSent=False,
                                siteKey=RECAPTCHA_SITE_KEY,
                                recaptcha=RECAPTCHA,
                            )
        case False:
            Log.danger(
                f"{request.remote_addr} tried to verify his account without being logged in"
            )  # Log a message with level 1 indicating the user is not logged in
            return redirect("/")  # Redirect to homepage if user is not logged in
