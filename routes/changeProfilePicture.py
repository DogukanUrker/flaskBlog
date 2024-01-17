from helpers import (
    flash,
    session,
    sqlite3,
    request,
    message,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    render_template,
    changeProfilePictureForm,
)

changeProfilePictureBlueprint = Blueprint("changeProfilePicture", __name__)


@changeProfilePictureBlueprint.route("/changeprofilepicture", methods=["GET", "POST"])
def changeProfilePicture():
    match "userName" in session:
        case True:
            form = changeProfilePictureForm(request.form)
            match request.method == "POST":
                case True:
                    newProfilePictureSeed = request.form["newProfilePictureSeed"]
                    newProfilePicture = f"https://api.dicebear.com/7.x/identicon/svg?seed={newProfilePictureSeed}&radius=10"
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """update users set profilePicture = ? where userName = ? """,
                        [(newProfilePicture), (session["userName"])],
                    )
                    connection.commit()
                    message(
                        "2",
                        f'USER: "{session["userName"]}" CHANGED HIS PROFILE PICTURE TO "{newProfilePicture}"',
                    )
                    flash("profile picture changed", "success")
                    return redirect(f"/changeprofilepicture")
            return render_template("changeProfilePicture.html", form=form)
        case False:
            return redirect("/")
