from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
    changeProfilePictureForm,
)

changeProfilePictureBlueprint = Blueprint("changeProfilePicture", __name__)


@changeProfilePictureBlueprint.route("/changeprofilepicture", methods=["GET", "POST"])
def changeProfilePicture():
    match "userName" in session:
        case True:
            form = changeProfilePictureForm(request.form)
            if request.method == "POST":
                newProfilePictureSeed = request.form["newProfilePictureSeed"]
                newProfilePicture = f"https://api.dicebear.com/7.x/identicon/svg?seed={newProfilePictureSeed}&radius=10"
                connection = sqlite3.connect("db/users.db")
                cursor = connection.cursor()
                cursor.execute(
                    f'update users set profilePicture = "{newProfilePicture}" where userName = "{session["userName"]}" '
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
