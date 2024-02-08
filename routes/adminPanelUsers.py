# Import the necessary modules and functions
from modules import (
    sqlite3,
    session,
    request,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    changeUserRole,
    render_template,
)
from delete import deleteUser

# Create a blueprint for the admin panel users route
adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


@adminPanelUsersBlueprint.route("/admin/users", methods=["GET", "POST"])
@adminPanelUsersBlueprint.route("/adminpanel/users", methods=["GET", "POST"])
def adminPanelUsers():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            # Connect to the users database and get the user role
            connection = sqlite3.connect(DB_USERS_ROOT)
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
                            # Delete the user from the database
                            deleteUser(request.form["userName"])
                    # Check if the user role change button is clicked
                    match "userRoleChangeButton" in request.form:
                        case True:
                            # Change the user role in the database
                            changeUserRole(request.form["userName"])
            # Check if the user role is admin
            match role == "admin":
                case True:
                    # Connect to the users database and get all the users
                    connection = sqlite3.connect(DB_USERS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute("select * from users")
                    users = cursor.fetchall()
                    # Render the admin panel users template with the users data
                    return render_template(
                        "adminPanelUsers.html.jinja",
                        users=users,
                    )
                case False:
                    # Redirect to the home page
                    return redirect("/")
        case False:
            # Redirect to the login page
            return redirect("/")
