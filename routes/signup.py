# Import the necessary modules and functions
from modules import (
    Log,
    ssl,
    abort,
    flash,
    session,
    sqlite3,
    request,
    smtplib,
    redirect,
    APP_NAME,
    SMTP_PORT,
    SMTP_MAIL,
    RECAPTCHA,
    addPoints,
    Blueprint,
    encryption,
    SignUpForm,
    SMTP_SERVER,
    EmailMessage,
    requestsPost,
    REGISTRATION,
    SMTP_PASSWORD,
    DB_USERS_ROOT,
    render_template,
    currentTimeStamp,
    RECAPTCHA_SIGN_UP,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
)

# Create a blueprint for the signup route
signUpBlueprint = Blueprint("signup", __name__)


# Define the route handler for the signup page
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
    # Check if registration is enabled
    match REGISTRATION:
        # If registration is enabled
        case True:
            # Check if the user is already logged in
            match "userName" in session:
                # If user is already logged in, redirect to homepage
                case True:
                    Log.danger(f'USER: "{session["userName"]}" ALREADY LOGGED IN')
                    return redirect("/")
                # If user is not logged in
                case False:
                    # Create sign up form object
                    form = SignUpForm(request.form)
                    # Check if request method is POST (form submitted)
                    match request.method == "POST":
                        # If form is submitted
                        case True:
                            # Extract form data
                            userName = request.form["userName"]
                            email = request.form["email"]
                            password = request.form["password"]
                            passwordConfirm = request.form["passwordConfirm"]
                            # Remove spaces from username
                            userName = userName.replace(" ", "")
                            # Connect to the database
                            connection = sqlite3.connect(DB_USERS_ROOT)
                            cursor = connection.cursor()
                            # Fetch existing usernames and emails from the database
                            cursor.execute("select userName from users")
                            users = str(cursor.fetchall())
                            cursor.execute("select email from users")
                            mails = str(cursor.fetchall())
                            # Check if username and email are available
                            match not userName in users and not email in mails:
                                # If username and email are available
                                case True:
                                    # Check if passwords match
                                    match passwordConfirm == password:
                                        # If passwords match
                                        case True:
                                            # Check if username contains only ASCII characters
                                            match userName.isascii():
                                                # If username contains only ASCII characters
                                                case True:
                                                    # Hash the password
                                                    password = encryption.hash(password)
                                                    # Connect to the database
                                                    connection = sqlite3.connect(
                                                        DB_USERS_ROOT
                                                    )
                                                    # Check if reCAPTCHA is enabled for sign up
                                                    match RECAPTCHA and RECAPTCHA_SIGN_UP:
                                                        # If reCAPTCHA is enabled
                                                        case True:
                                                            # Verify reCAPTCHA response
                                                            secretResponse = request.form[
                                                                "g-recaptcha-response"
                                                            ]
                                                            verifyResponse = requestsPost(
                                                                url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                            ).json()
                                                            # If reCAPTCHA verification is successful
                                                            match verifyResponse[
                                                                "success"
                                                            ] == True or verifyResponse[
                                                                "score"
                                                            ] > 0.5:
                                                                # If reCAPTCHA verification is successful
                                                                case True:
                                                                    Log.success(
                                                                        f"SIGN UP RECAPTCHA | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
                                                                    )
                                                                    # Insert user data into the database
                                                                    cursor = (
                                                                        connection.cursor()
                                                                    )
                                                                    cursor.execute(
                                                                        f"""
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
                                                                    # Log user addition
                                                                    Log.success(
                                                                        f'USER: "{userName}" ADDED TO DATABASE',
                                                                    )
                                                                    # Store username in session (log user in)
                                                                    session[
                                                                        "userName"
                                                                    ] = userName
                                                                    # Add points to the user
                                                                    addPoints(
                                                                        1,
                                                                        session[
                                                                            "userName"
                                                                        ],
                                                                    )
                                                                    # Log user login
                                                                    Log.success(
                                                                        f'USER: "{userName}" LOGGED IN',
                                                                    )
                                                                    # Flash success message
                                                                    flash(
                                                                        f"Welcome {userName}",
                                                                        "success",
                                                                    )
                                                                    # Set up email server connection
                                                                    context = (
                                                                        ssl.create_default_context()
                                                                    )
                                                                    server = (
                                                                        smtplib.SMTP(
                                                                            SMTP_SERVER,
                                                                            SMTP_PORT,
                                                                        )
                                                                    )
                                                                    server.ehlo()
                                                                    server.starttls(
                                                                        context=context
                                                                    )
                                                                    server.ehlo()
                                                                    server.login(
                                                                        SMTP_MAIL,
                                                                        SMTP_PASSWORD,
                                                                    )
                                                                    # Compose email message
                                                                    mail = (
                                                                        EmailMessage()
                                                                    )
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
                                                                    mail["Subject"] = (
                                                                        f"Welcome to {APP_NAME}"
                                                                    )
                                                                    mail["From"] = (
                                                                        SMTP_MAIL
                                                                    )
                                                                    mail["To"] = email
                                                                    # Send email
                                                                    server.send_message(
                                                                        mail
                                                                    )
                                                                    server.quit()
                                                                    # Redirect user for further verification
                                                                    return redirect(
                                                                        "/verifyUser/codesent=false"
                                                                    )
                                                                # If reCAPTCHA verification fails
                                                                case False:
                                                                    Log.danger(
                                                                        f"SIGN UP | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
                                                                    )
                                                                    abort(401)
                                                        # If reCAPTCHA is not enabled
                                                        case False:
                                                            # Insert user data into the database
                                                            cursor = connection.cursor()
                                                            cursor.execute(
                                                                f"""
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
                                                            # Log user addition
                                                            Log.success(
                                                                f'USER: "{userName}" ADDED TO DATABASE',
                                                            )
                                                            # Store username in session (log user in)
                                                            session["userName"] = (
                                                                userName
                                                            )
                                                            # Add points to the user
                                                            addPoints(
                                                                1, session["userName"]
                                                            )
                                                            # Log user login
                                                            Log.success(
                                                                f'USER: "{userName}" LOGGED IN',
                                                            )
                                                            # Flash success message
                                                            flash(
                                                                f"Welcome {userName}",
                                                                "success",
                                                            )
                                                            # Set up email server connection
                                                            context = (
                                                                ssl.create_default_context()
                                                            )
                                                            server = smtplib.SMTP(
                                                                SMTP_SERVER, SMTP_PORT
                                                            )
                                                            server.ehlo()
                                                            server.starttls(
                                                                context=context
                                                            )
                                                            server.ehlo()
                                                            server.login(
                                                                SMTP_MAIL, SMTP_PASSWORD
                                                            )
                                                            # Compose email message
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
                                                            mail["Subject"] = (
                                                                f"Welcome to {APP_NAME}"
                                                            )
                                                            mail["From"] = SMTP_MAIL
                                                            mail["To"] = email
                                                            # Send email
                                                            server.send_message(mail)
                                                            server.quit()
                                                            # Redirect user for further verification
                                                            return redirect(
                                                                "/verifyUser/codesent=false"
                                                            )
                                                # If username contains non-ASCII characters
                                                case False:
                                                    Log.danger(
                                                        f'USERNAME: "{userName}" DOES NOT FITS ASCII CHARACTERS',
                                                    )
                                                    # Flash error message
                                                    flash(
                                                        "username does not fit ascii charecters",
                                                        "error",
                                                    )
                                        # If passwords do not match
                                        case False:
                                            Log.danger(" PASSWORDS MUST MATCH ")
                                            # Flash error message
                                            flash("password must match", "error")
                            # If username or email is not available
                            match userName in users and email in mails:
                                case True:
                                    Log.danger(
                                        f'"{userName}" & "{email}" IS UNAVAILABLE '
                                    )
                                    # Flash error message
                                    flash(
                                        "This username and email is unavailable.",
                                        "error",
                                    )
                            match not userName in users and email in mails:
                                case True:
                                    Log.danger(f'THIS EMAIL "{email}" IS UNAVAILABLE ')
                                    # Flash error message
                                    flash("This email is unavailable.", "error")
                            match userName in users and not email in mails:
                                case True:
                                    Log.danger(
                                        f'THIS USERNAME "{userName}" IS UNAVAILABLE ',
                                    )
                                    # Flash error message
                                    flash("This username is unavailable.", "error")
                    # Render sign up template with form data
                    return render_template(
                        "signup.html.jinja",
                        form=form,
                        hideSignUp=True,
                        siteKey=RECAPTCHA_SITE_KEY,
                        recaptcha=RECAPTCHA,
                    )
        # If registration is disabled
        case False:
            # Redirect to homepage
            return redirect("/")
