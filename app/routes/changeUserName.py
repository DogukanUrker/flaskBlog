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
from utils.forms.ChangeUserNameForm import ChangeUserNameForm
from utils.log import Log

change_user_name_blueprint = Blueprint("changeUserName", __name__)


@change_user_name_blueprint.route("/changeusername", methods=["GET", "POST"])
def change_user_name():
    """
    Checks if the user is logged in:
    If the user is not logged in, they are redirected to the homepage.

    Checks if the user has submitted a new username:
    If the user has submitted a new username, the new username is checked to ensure it meets the requirements.

    If the new username meets the requirements:
    The user's details are updated in the database.
    The user is redirected to their profile page.

    If the new username does not meet the requirements:
    An error message is displayed.

    Returns:
    The change username template with the form.
    """

    if "user_name" in session:
        form = ChangeUserNameForm(request.form)

        if request.method == "POST":
            new_user_name = request.form["new_user_name"]
            new_user_name = new_user_name.replace(" ", "")
            Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

            connection = sqlite3.connect(Settings.DB_USERS_ROOT)
            connection.set_trace_callback(Log.database)
            cursor = connection.cursor()
            cursor.execute(
                """select user_name from users where user_name = ? """,
                [(new_user_name)],
            )
            user_name_check = cursor.fetchone()

            if new_user_name.isascii():
                if new_user_name == session["user_name"]:
                    flash_message(
                        page="changeUserName",
                        message="same",
                        category="error",
                        language=session["language"],
                    )
                else:
                    if user_name_check is None:
                        cursor.execute(
                            """update users set user_name = ? where user_name = ? """,
                            [(new_user_name), (session["user_name"])],
                        )
                        connection.commit()

                        connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
                        connection.set_trace_callback(Log.database)
                        cursor = connection.cursor()
                        cursor.execute(
                            """update posts set Author = ? where author = ? """,
                            [(new_user_name), (session["user_name"])],
                        )
                        connection.commit()

                        connection = sqlite3.connect(Settings.DB_COMMENTS_ROOT)
                        connection.set_trace_callback(Log.database)
                        cursor = connection.cursor()
                        cursor.execute(
                            """update comments set user = ? where user = ? """,
                            [(new_user_name), (session["user_name"])],
                        )
                        connection.commit()
                        Log.success(
                            f'User: "{session["user_name"]}" changed his username to "{new_user_name}"'
                        )
                        session["user_name"] = new_user_name
                        flash_message(
                            page="changeUserName",
                            message="success",
                            category="success",
                            language=session["language"],
                        )
                        return redirect(f"/user/{new_user_name.lower()}")
                    else:
                        flash_message(
                            page="changeUserName",
                            message="taken",
                            category="error",
                            language=session["language"],
                        )
            else:
                flash_message(
                    page="changeUserName",
                    message="ascii",
                    category="error",
                    language=session["language"],
                )

        return render_template(
            "changeUserName.html",
            form=form,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to change his username without being logged in"
        )

        return redirect("/")
