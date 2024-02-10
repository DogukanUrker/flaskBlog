# Import necessary modules and functions
from modules import (
    sqlite3,  # SQLite database module
    session,  # Session handling module
    redirect,  # Redirect function
    Blueprint,  # Blueprint for defining routes
    DB_USERS_ROOT,  # Path to the users database
    render_template,  # Template rendering function
)

# Create a blueprint for the admin panel route
adminPanelBlueprint = Blueprint("adminPanel", __name__)


# Define route for the admin panel
@adminPanelBlueprint.route("/admin")
def adminPanel():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            # Connect to the database and get the user role
            connection = sqlite3.connect(DB_USERS_ROOT)
            cursor = connection.cursor()
            cursor.execute(
                """select role from users where userName = ? """,
                [(session["userName"])],
            )
            role = cursor.fetchone()[0]
            # Check if the user role is admin
            match role == "admin":
                case True:
                    # Render the admin panel template
                    return render_template("adminPanel.html.jinja")
                case False:
                    # Redirect to the home page if the user is not an admin
                    return redirect("/")
        case False:
            # Redirect to the login page if the user is not logged in
            return redirect("/")
