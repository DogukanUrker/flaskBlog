from helpers import (
    abort,
    message,
    request,
    sqlite3,
    session,
    redirect,
    Blueprint,
    RECAPTCHA,
    requestsPost,
    DB_USERS_ROOT,
    render_template,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_DELETE_USER,
)
from delete import deleteUser

accountSettingsBlueprint = Blueprint("accountSettings", __name__)


@accountSettingsBlueprint.route("/accountsettings", methods=["GET", "POST"])
def accountSettings():
    match "userName" in session:
        case True:
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select userName from users where userName = ? """,
                [(session["userName"])],
            )
            user = cursor.fetchall()
            match request.method == "POST":
                case True:
                    match RECAPTCHA and RECAPTCHA_DELETE_USER:
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
                                    message("2",f"USER DELETE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                    deleteUser(user[0][0])
                                    return redirect(f"/")
                                case False:
                                    message("1",f"USER DELETE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                    abort(401)
                        case False:
                            deleteUser(user[0][0])
                            return redirect(f"/")
            return render_template("accountSettings.html", user=user, siteKey=RECAPTCHA_SITE_KEY, recaptcha=RECAPTCHA,)
        case False:
            return redirect("/login/redirect=&accountsettings")
