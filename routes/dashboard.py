# Import necessary modules and functions
from modules import (
    Log,  # Custom logging module
    flash,  # Flash messaging module
    Delete,  # Function for deleting data
    url_for,  # URL building function
    request,  # Request handling module
    session,  # Session handling module
    sqlite3,  # SQLite database module
    redirect,  # Redirect function
    Blueprint,  # Blueprint for defining routes
    DB_POSTS_ROOT,  # Path to the posts database
    DB_COMMENTS_ROOT,  # Path to the comments database
    render_template,  # Template rendering function
)

# Create a blueprint for the dashboard route
dashboardBlueprint = Blueprint("dashboard", __name__)


# Define a route for the dashboard
@dashboardBlueprint.route("/dashboard/<userName>", methods=["GET", "POST"])
def dashboard(userName):
    # Check if the user is logged in
    match "userName" in session:
        case True:
            # Check if the session user name matches the route user name
            match session["userName"].lower() == userName.lower():
                case True:
                    # Check if the request method is POST
                    match request.method == "POST":
                        case True:
                            # Check if the post delete button is clicked
                            match "postDeleteButton" in request.form:
                                case True:
                                    # Delete the post from the database
                                    Delete.post(request.form["postID"])
                                    # Redirect to the same route with a 301 status code
                                    return (
                                        redirect(
                                            url_for(
                                                "dashboard.dashboard", userName=userName
                                            )
                                        ),
                                        301,
                                    )
                    Log.sql(
                        f"Connecting to '{DB_POSTS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the posts database
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    # Query the posts database for the posts authored by the session user name
                    cursor.execute(
                        """select * from posts where author = ? order by timeStamp desc""",
                        [(session["userName"])],
                    )
                    posts = cursor.fetchall()
                    Log.sql(
                        f"Connecting to '{DB_COMMENTS_ROOT}' database"
                    )  # Log the database connection is started
                    # Connect to the comments database
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    connection.set_trace_callback(
                        Log.sql
                    )  # Set the trace callback for the connection
                    cursor = connection.cursor()
                    # Query the comments database for the comments made by the route user name
                    cursor.execute(
                        """select * from comments where lower(user) = ? order by timeStamp desc""",
                        [(userName.lower())],
                    )
                    comments = cursor.fetchall()
                    # Initialize a flag for showing posts
                    match posts:
                        case []:
                            showPosts = False
                        case _:
                            showPosts = True
                    # Initialize a flag for showing comments
                    match comments:
                        case []:
                            showComments = False
                        case _:
                            showComments = True
                    # Render the dashboard template with the posts, comments, showPosts and showComments data
                    return render_template(
                        "/dashboard.html.jinja",
                        posts=posts,
                        comments=comments,
                        showPosts=showPosts,
                        showComments=showComments,
                    )
                case False:
                    # Log a message that the dashboard does not belong to the session user name
                    Log.danger(
                        f'User: "{session["userName"]}" tried to login to another users dashboard',
                    )
                    # Redirect to the dashboard of the session user name
                    return redirect(f'/dashboard/{session["userName"].lower()}')
        case False:
            # Log a message that the dashboard cannot be accessed without user login
            Log.danger(
                f"{request.remote_addr} tried to access the dashboard without login"
            )
            # Flash an error message to the user
            flash("You need login for reach to dashboard.", "error")
            # Redirect to the login page with the dashboard and user as the next destination
            return redirect("/login/redirect=&dashboard&user")
