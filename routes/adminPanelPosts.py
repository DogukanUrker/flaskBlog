# Import necessary modules and functions
from modules import (
    Log,  # A class for logging messages
    Delete,  # Function for deleting posts
    sqlite3,  # SQLite database module
    session,  # Session handling module
    request,  # Request handling module
    redirect,  # Redirect function
    Blueprint,  # Blueprint for defining routes
    DB_POSTS_ROOT,  # Path to the posts database
    DB_USERS_ROOT,  # Path to the users database
    render_template,  # Template rendering function
)

# Create a blueprint for the admin panel posts route
adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


# Define routes for the admin panel posts
@adminPanelPostsBlueprint.route("/admin/posts", methods=["GET", "POST"])
@adminPanelPostsBlueprint.route("/adminpanel/posts", methods=["GET", "POST"])
def adminPanelPosts():
    # Check if the user is logged in
    match "userName" in session:
        case True:
            Log.info(
                f"Admin: {session['userName']} reached to posts admin panel"
            )  # Log a message that the admin reached to posts admin panel
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
                    # Check if the post delete button is clicked
                    match "postDeleteButton" in request.form:
                        case True:
                            Log.info(
                                f"Admin: {session['userName']} deleted post: {request.form['postID']}"
                            )  # Log a message that admin deleted a post
                            # Delete the post from the database
                            Delete.post(request.form["postID"])
            # Check if the user role is admin
            match role == "admin":
                case True:
                    Log.sql(
                        f"Connecting to '{DB_POSTS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the posts database and get all the posts
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    cursor.execute("select * from posts order by timeStamp desc")
                    posts = cursor.fetchall()
                    # Log a message that admin panel posts page loaded with post data
                    Log.info(
                        f"Rendering dashboard.html.jinja: params: posts={len(posts)} and showPosts=True"
                    )
                    # Render the dashboard template with the posts data and showPosts flag
                    return render_template(
                        "dashboard.html.jinja", posts=posts, showPosts=True
                    )
                case False:
                    Log.danger(
                        f"{request.remote_addr} tried to reach post admin panel without being admin"
                    )  # Log a message that the user tried to reach admin panel without being admin
                    # Redirect to the home page if the user is not an admin
                    return redirect("/")
        case False:
            Log.danger(
                f"{request.remote_addr} tried to reach post admin panel being logged in"
            )  # Log a message that the user tried to reach admin panel without being logged in
            # Redirect to the login page if the user is not logged in
            return redirect("/")
