import sqlite3

from flask import redirect, session
from settings import DB_USERS_ROOT
from utils.log import Log


def changeUserRole(userName):
    """
    Changes the role of the user with the specified username.
    """
    userName = userName.lower()
    Log.database(f"Connecting to '{DB_USERS_ROOT}' database")
    connection = sqlite3.connect(DB_USERS_ROOT)
    connection.set_trace_callback(Log.database)
    cursor = connection.cursor()
    cursor.execute(
        """select role from users where lower(userName) = ? """,
        [(userName)],
    )
    role = cursor.fetchone()[0]
    match role:
        case "admin":
            newRole = "user"
        case "user":
            newRole = "admin"
    cursor.execute(
        """update users set role = ? where lower(userName) = ? """,
        [(newRole), (userName)],
    )
    Log.success(
        f'Admin: "{session["userName"]}" changed user: "{userName}"s role to "{newRole}" ',
    )
    connection.commit()
    match session["userName"].lower() == userName:
        case True:
            Log.success(f'Admin: "{session["userName"]}" changed his role to "user"')
            return redirect("/")
