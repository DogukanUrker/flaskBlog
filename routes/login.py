from modules import (
    abort,
    flash,
    LOG_IN,
    session,
    request,
    sqlite3,
    message,
    redirect,
    RECAPTCHA,
    addPoints,
    Blueprint,
    LoginForm,
    encryption,
    requestsPost,
    DB_USERS_ROOT,
    render_template,
    RECAPTCHA_LOGIN,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
)

loginBlueprint = Blueprint("login", __name__)


@loginBlueprint.route("/login/redirect=<direct>", methods=["GET", "POST"])
def login(direct):
    """
    This function handles the login process for the website.

    Args:
        direct (str): The direct link to redirect to after login.

    Returns:
        tuple: A tuple containing the redirect response and status code.

    Raises:
        401: If the login is unsuccessful.
    """
    direct = direct.replace("&", "/")
    match LOG_IN:
        case True:
            match "userName" in session:
                case True:
                    message("1", f'USER: "{session["userName"]}" ALREADY LOGGED IN')
                    return (
                        redirect(direct),
                        301,
                    )
                case False:
                    form = LoginForm(request.form)
                    match request.method == "POST":
                        case True:
                            userName = request.form["userName"]
                            password = request.form["password"]
                            userName = userName.replace(" ", "")
                            connection = sqlite3.connect(DB_USERS_ROOT)
                            cursor = connection.cursor()
                            cursor.execute(
                                """select * from users where lower(userName) = ? """,
                                [(userName.lower())],
                            )
                            user = cursor.fetchone()
                            match not user:
                                case True:
                                    message("1", f'USER: "{userName}" NOT FOUND')
                                    flash("user not found", "error")
                                case _:
                                    match encryption.verify(password, user[3]):
                                        case True:
                                            match RECAPTCHA and RECAPTCHA_LOGIN:
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
                                                            # Logs the user in if the reCAPTCHA verification is successful
                                                            message(
                                                                "2",
                                                                f"LOGIN RECAPTCHA | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
                                                            )
                                                            session["userName"] = user[
                                                                1
                                                            ]
                                                            session["userRole"] = user[
                                                                5
                                                            ]
                                                            addPoints(
                                                                1, session["userName"]
                                                            )
                                                            message(
                                                                "2",
                                                                f'USER: "{user[1]}" LOGGED IN',
                                                            )
                                                            flash(
                                                                f"Welcome {user[1]}",
                                                                "success",
                                                            )
                                                            return (
                                                                redirect(direct),
                                                                301,
                                                            )

                                                        case False:
                                                            # Returns an unauthorized error if the reCAPTCHA verification is unsuccessful
                                                            message(
                                                                "1",
                                                                f"LOGIN RECAPTCHA | VERIFICATION: {verifyResponse['success']} | VERIFICATION SCORE: {verifyResponse['score']}",
                                                            )
                                                            abort(401)

                                                case False:
                                                    # Logs the user in if reCAPTCHA is not required
                                                    session["userName"] = user[1]
                                                    session["userRole"] = user[5]
                                                    addPoints(1, session["userName"])
                                                    message(
                                                        "2",
                                                        f'USER: "{user[1]}" LOGGED IN',
                                                    )
                                                    flash(
                                                        f"Welcome {user[1]}", "success"
                                                    )
                                                    return (
                                                        redirect(direct),
                                                        301,
                                                    )

                                        case _:
                                            # Returns an incorrect password error if the password is incorrect
                                            message("1", "WRONG PASSWORD")
                                            flash("wrong  password", "error")
                    return render_template(
                        "login.html.jinja",
                        form=form,
                        hideLogin=True,
                        siteKey=RECAPTCHA_SITE_KEY,
                        recaptcha=RECAPTCHA,
                    )
        case False:
            return (
                redirect(direct),
                301,
            )
