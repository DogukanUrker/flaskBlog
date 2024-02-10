# Import necessary modules and functions
from modules import (
    Delete,  # Function for deleting users
    sqlite3,  # SQLite database module
    session,  # Session handling module
    request,  # Request handling module
    redirect,  # Redirect function
    Blueprint,  # Blueprint for defining routes
    DB_USERS_ROOT,  # Path to the users database
    changeUserRole,  # Function for changing user roles
    render_template,  # Template rendering function
)

# Create a blueprint for the admin panel users route
adminPanelUsersBlueprint = Blueprint("adminPanelUsers", __name__)


# Define routes for the admin panel users
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
                            Delete.user(request.form["userName"])
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
                    # Redirect to the home page if the user is not an admin
                    return redirect("/")
        case False:
            # Redirect to the login page if the user is not logged in
            return redirect("/")
