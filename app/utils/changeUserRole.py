import sqlite3

from flask import redirect, session
from settings import Settings
from utils.log import Log


def changeUserRole(userName):
    """
    Changes the role of the user with the specified username.
    """
    userName = userName.lower()
    Log.database(f"Connecting to '{Settings.DB_USERS_ROOT}' database")
    connection = sqlite3.connect(Settings.DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    cursor.execute(
        """select role from users where lower(userName) = ? """,
        [(userName)],
    )
    role = cursor.fetchone()[0]
    if role == "admin":
        newRole = "user"
    elif role == "user":
        newRole = "admin"
    cursor.execute(
        """update users set role = ? where lower(userName) = ? """,
        [(newRole), (userName)],
    )
    Log.success(
        f'Admin: "{session["userName"]}" changed user: "{userName}"s role to "{newRole}" ',
    )
    connection.commit()
    if session["userName"].lower() == userName:
        Log.success(f'Admin: "{session["userName"]}" changed his role to "user"')
        return redirect("/")
