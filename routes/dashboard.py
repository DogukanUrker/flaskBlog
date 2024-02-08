# Import the necessary modules and functions
from modules import (
    Log,
    flash,
    Delete,
    url_for,
    request,
    session,
    sqlite3,
    redirect,
    Blueprint,
    DB_POSTS_ROOT,
    DB_COMMENTS_ROOT,
    render_template,
)

# Create a blueprint for the dashboard route
dashboardBlueprint = Blueprint("dashboard", __name__)


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
                                    Delete.user(request.form["postID"])
                                    # Redirect to the same route with a 301 status code
                                    return (
                                        redirect(
                                            url_for(
                                                "dashboard.dashboard", userName=userName
                                            )
                                        ),
                                        301,
                                    )
                    # Connect to the posts database
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    cursor = connection.cursor()
                    # Query the posts database for the posts authored by the session user name
                    cursor.execute(
                        """select * from posts where author = ? order by timeStamp desc""",
                        [(session["userName"])],
                    )
                    posts = cursor.fetchall()
                    # Connect to the comments database
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
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
                        f'THIS IS DASHBOARD NOT BELONGS TO USER: "{session["userName"]}"',
                    )
                    # Redirect to the dashboard of the session user name
                    return redirect(f'/dashboard/{session["userName"].lower()}')
        case False:
            # Log a message that the dashboard cannot be accessed without user login
            Log.danger("DASHBOARD CANNOT BE ACCESSED WITHOUT USER LOGIN")
            # Flash an error message to the user
            flash("you need login for reach to dashboard", "error")
            # Redirect to the login page with the dashboard and user as the next destination
            return redirect("/login/redirect=&dashboard&user")
