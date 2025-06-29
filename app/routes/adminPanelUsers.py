# Import necessary modules and functions
import sqlite3
from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    session,
)
from requests import post as requestsPost
from constants import (
    DB_USERS_ROOT,
    RECAPTCHA,
    RECAPTCHA_DELETE_USER,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.log import Log
from utils.delete import Delete
from utils.flashMessage import flashMessage
from utils.changeUserRole import changeUserRole

# Create a blueprint for the admin panel users route
adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


# Define routes for the admin panel users
@adminPanelUsersBlueprint.route("/admin/users", methods=["GET", "POST"])
@adminPanelUsersBlueprint.route("/adminpanel/users", methods=["GET", "POST"])
def adminPanelUsers():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            Log.info(
                f"Admin: {session['userName']} reached to users admin panel"
            )  # Log a message that the admin reached to users admin panel
            Log.database(
                f"Connecting to '{DB_USERS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the users database and get the user role
            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(
                Log.database
            )  # Set the trace callback for the connection
            cursor = connection.cursor()
            cursor.execute(
                """select role from users where userName = ? """,
                [(session["userName"])],
            )
            role = cursor.fetchone()[0]
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Check if the user delete button is clicked
                    match "userDeleteButton" in request.form:
                        case True:
                            Log.info(
                                f"Admin: {session['userName']} deleted user: {request.form['userName']}"
                            )  # Log a message that admin deleted a user
                            # Delete the user from the database
                            Delete.user(request.form["userName"])
                    # Check if the user role change button is clicked
                    match "userRoleChangeButton" in request.form:
                        case True:
                            Log.info(
                                f"Admin: {session['userName']} changed {request.form['userName']}'s role"
                            )  # Log a message that admin changed a user's role
                            # Change the user role in the database
                            changeUserRole(request.form["userName"])
            # Check if the user role is admin
            match role == "admin":
                case True:
                    Log.database(
                        f"Connecting to '{DB_USERS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the users database and get all the users
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    connection.set_trace_callback(
                        Log.database
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    cursor.execute("select * from users")
                    users = cursor.fetchall()
                    # Log a message that admin panel users page loaded with user data
                    Log.info(
                        f"Rendering adminPanelUsers.html.jinja: params: users={users}"
                    )
                    # Render the admin panel users template with the users data
                    return render_template(
                        "adminPanelUsers.html.jinja",
                        users=users,
                    )
                case False:
                    Log.error(
                        f"{request.remote_addr} tried to reach user admin panel without being admin"
                    )  # Log a message that the user tried to reach admin panel without being admin
                    # Redirect to the home page if the user is not an admin
                    return redirect("/")
        case False:
            Log.error(
                f"{request.remote_addr} tried to reach user admin panel being logged in"
            )  # Log a message that the user tried to reach admin panel without being logged in
            # Redirect to the login page if the user is not logged in
            return redirect("/")
