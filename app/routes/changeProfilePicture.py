import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import Settings
from utils.flashMessage import flash_message
from utils.forms.ChangeProfilePictureForm import ChangeProfilePictureForm
from utils.log import Log

change_profile_picture_blueprint = Blueprint("changeProfilePicture", __name__)


@change_profile_picture_blueprint.route("/changeprofilepicture", methods=["GET", "POST"])
def change_profile_picture():
    if "user_name" in session:
        form = ChangeProfilePictureForm(request.form)

        if request.method == "POST":
            new_profile_picture_seed = request.form["new_profile_picture_seed"]

            new_profile_picture = f"https://api.dicebear.com/7.x/identicon/svg?seed={new_profile_picture_seed}&radius=10"
            Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")
            Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

            connection = sqlite3.connect(Settings.DB_USERS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()

            cursor.execute(
                """update users set profile_picture = ? where user_name = ? """,
                [(new_profile_picture), (session["user_name"])],
            )
            connection.commit()

            Log.success(
                f'User: "{session["user_name"]}" changed his profile picture to "{new_profile_picture}"',
            )
            flash_message(
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
