import sqlite3

from flask import redirect, session
from settings import Settings
from utils.log import Log


def change_user_role(user_name):
    """
    Changes the role of the user with the specified username.
    """
    user_name = user_name.lower()
    Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")
    connection = sqlite3.connect(Settings.DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    cursor.execute(
        """select role from users where lower(user_name) = ? """,
        [(user_name)],
    )
    role = cursor.fetchone()[0]
    if role == "admin":
        new_role = "user"
    elif role == "user":
        new_role = "admin"
    cursor.execute(
        """update users set role = ? where lower(user_name) = ? """,
        [(new_role), (user_name)],
    )
    Log.success(
        f'Admin: "{session["user_name"]}" changed user: "{user_name}"s role to "{new_role}" ',
    )
    connection.commit()
    if session["user_name"].lower() == user_name:
        Log.success(f'Admin: "{session["user_name"]}" changed his role to "user"')
        return redirect("/")
