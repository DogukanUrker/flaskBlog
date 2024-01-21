# Import the necessary modules and functions
from helpers import (
    sqlite3,
    session,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    render_template,
)

# Create a blueprint for the admin panel route
adminPanelBlueprint = Blueprint("adminPanel", __name__)


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
                    return render_template("adminPanel.html")
                case False:
                    # Redirect to the home page
                    return redirect("/")
        case False:
            # Redirect to the login page
            return redirect("/")
