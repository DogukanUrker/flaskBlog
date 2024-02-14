# Import necessary modules and functions
from modules import (
    Log,  # A class for logging messages
    Delete,  # Function for deleting comments
    request,  # Request handling module
    sqlite3,  # SQLite database module
    session,  # Session handling module
    redirect,  # Redirect function
    Blueprint,  # Blueprint for defining routes
    DB_USERS_ROOT,  # Path to the users database
    render_template,  # Template rendering function
    DB_COMMENTS_ROOT,  # Path to the comments database
)

# Create a blueprint for the admin panel comments route
adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


# Define routes for the admin panel comments
@adminPanelCommentsBlueprint.route("/admin/comments", methods=["GET", "POST"])
@adminPanelCommentsBlueprint.route("/adminpanel/comments", methods=["GET", "POST"])
def adminPanelComments():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            Log.info(
                f"Admin: {session['userName']} reached to comments admin panel"
            )  # Log a message that the admin reached to comments admin panel
            Log.sql(
                f"Connecting to '{DB_USERS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the users database and get the user role
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
            # Check if the request method is POST
            match request.method == "POST":
                case True:
                    # Check if the comment delete button is clicked
                    match "commentDeleteButton" in request.form:
                        case True:
                            Log.info(
                                f"Admin: {session['userName']} deleted comment: {request.form['commentID']}"
                            )  # Log a message that admin deleted a comment
                            # Delete the comment from the database
                            Delete.comment(request.form["commentID"])
                    # Redirect to the same route
                    return redirect(f"/admin/comments")
            # Check if the user role is admin
            match role == "admin":
                case True:
                    Log.sql(
                        f"Connecting to '{DB_COMMENTS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the comments database and get all the comments
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    cursor.execute("select * from comments order by timeStamp desc")
                    comments = cursor.fetchall()
                    # Log a message that admin panel comments page loaded with comment data
                    Log.info(
                        f"Rendering adminPanelComments.html.jinja: params: comments={comments}"
                    )
                    # Render the admin panel comments template with the comments data
                    return render_template(
                        "adminPanelComments.html.jinja", comments=comments
                    )
                case False:
                    Log.danger(
                        f"{request.remote_addr} tried to reach comment admin panel without being admin"
                    )  # Log a message that the user tried to reach admin panel without being admin
                    # Redirect to the home page if the user is not an admin
                    return redirect("/")
        case False:
            Log.danger(
                f"{request.remote_addr} tried to reach comment admin panel being logged in"
            )  # Log a message that the user tried to reach admin panel without being logged in
            # Redirect to the login page if the user is not logged in
            return redirect("/")
