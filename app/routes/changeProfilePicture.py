import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import (
    DB_USERS_ROOT,
)
from utils.flashMessage import flashMessage
from utils.forms.ChangeProfilePictureForm import ChangeProfilePictureForm
from utils.log import Log

changeProfilePictureBlueprint = Blueprint("changeProfilePicture", __name__)


@changeProfilePictureBlueprint.route("/changeprofilepicture", methods=["GET", "POST"])
def changeProfilePicture():
    if "userName" in session:
        form = ChangeProfilePictureForm(request.form)

        if request.method == "POST":
            newProfilePictureSeed = request.form["newProfilePictureSeed"]

            newProfilePicture = f"https://api.dicebear.com/7.x/identicon/svg?seed={newProfilePictureSeed}&radius=10"
            Log.database(f"Connecting to '{DB_USERS_ROOT}' database")
            Log.database(f"Connecting to '{DB_USERS_ROOT}' database")

            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                """update users set profilePicture = ? where userName = ? """,
                [(newProfilePicture), (session["userName"])],
            )
            connection.commit()

            Log.success(
                f'User: "{session["userName"]}" changed his profile picture to "{newProfilePicture}"',
            )
            flashMessage(
                page="changeProfilePicture",
                message="success",
                category="success",
                language=session["language"],
            )

            return redirect("/changeprofilepicture")

        return render_template(
            "changeProfilePicture.html",
            form=form,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to change his profile picture without being logged in"
        )

        return redirect("/")
