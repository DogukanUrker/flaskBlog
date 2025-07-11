import sqlite3

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
)
from settings import Settings
from utils.flash_message import flash_message
from utils.forms.ChangeUserNameForm import ChangeUserNameForm
from utils.log import Log

change_user_name_blueprint = Blueprint("change_user_name", __name__)


@change_user_name_blueprint.route("/changeusername", methods=["GET", "POST"])
def change_user_name():
    """
    This function is the route for the change username page.
    It is used to change the user's username.

    Args:
        request.form (dict): the form data from the request

    Returns:
        render_template: a rendered template with the form
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
                """select * from users where lower(user_name) = ? """,
                [(new_user_name.lower())],
            )
            user = cursor.fetchone()

            if not user:
                Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")

                connection = sqlite3.connect(Settings.DB_USERS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()
                cursor.execute(
                    """update users set user_name = ? where user_name = ? """,
                    [(new_user_name), (session["user_name"])],
                )

                connection.commit()

                Log.database(f"Connecting to '{Settings.DB_POSTS_ROOT}' database")

                connection = sqlite3.connect(Settings.DB_POSTS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()
                cursor.execute(
                    """update posts set user_name = ? where user_name = ? """,
                    [(new_user_name), (session["user_name"])],
                )

                connection.commit()

                Log.database(f"Connecting to '{Settings.DB_COMMENTS_ROOT}' database")

                connection = sqlite3.connect(Settings.DB_COMMENTS_ROOT)
                connection.set_trace_callback(Log.database)
                cursor = connection.cursor()
                cursor.execute(
                    """update comments set user_name = ? where user_name = ? """,
                    [(new_user_name), (session["user_name"])],
                )

                connection.commit()

                Log.success(
                    f"User: {session['user_name']} changed his username to {new_user_name}",
                )

                session["user_name"] = new_user_name
                flash_message(
                    page="change_user_name",
                    message="success",
                    category="success",
                    language=session["language"],
                )

                return redirect("/account_settings")
            else:
                Log.error(f'User: "{new_user_name}" already exists')
                flash_message(
                    page="change_user_name",
                    message="exists",
                    category="error",
                    language=session["language"],
                )

        return render_template(
            "changeUserName.html",
            form=form,
        )
    else:
        Log.error(
            f"{request.remote_addr} tried to change his username without logging in"
        )
        flash_message(
            page="change_user_name",
            message="login",
            category="error",
            language=session["language"],
        )

        return redirect("/login/redirect=changeusername")
