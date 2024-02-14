# Import necessary modules and functions
from modules import (
    Log,  # A class for logging messages
    sqlite3,  # SQLite database module
    session,  # Session handling module
    request,  # Request handling module
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
            Log.sql(
                f"Connecting to '{DB_USERS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the database and get the user role
            connection = sqlite3.connect(DB_USERS_ROOT)
            connection.set_trace_callback(
                Log.sql
            )  # Set the trace callback for the connection
            cursor = connection.cursor()
            cursor.execute(
                """select role from users where userName = ? """,
                [(session["userName"])],
            )
            role = cursor.fetchone()[0]
            # Check if the user role is admin
            match role == "admin":
                case True:

                    # Log info message that the admin reached to the admin panel
                    Log.info(f'Admin: {session["userName"]} reached to the admin panel')
                    # Log a message that admin panel loaded
                    Log.info(f"Rendering adminPanel.html.jinja: params: None")
                    # Render the admin panel template
                    return render_template("adminPanel.html.jinja")
                case False:
                    Log.danger(
                        f"{request.remote_addr} tried to reach admin panel without being admin"
                    )  # Log a message that the user tried to reach admin panel without being admin
                    # Redirect to the home page if the user is not an admin
                    return redirect("/")
        case False:
            Log.danger(
                f"{request.remote_addr} tried to reach admin panel being logged in"
            )  # Log a message that the user tried to reach admin panel without being logged in
            # Redirect to the login page if the user is not logged in
            return redirect("/")
