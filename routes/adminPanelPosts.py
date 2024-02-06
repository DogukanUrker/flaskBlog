# Import the necessary modules and functions
from helpers import (
    sqlite3,
    session,
    request,
    redirect,
    Blueprint,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    render_template,
)
from delete import deletePost

# Create a blueprint for the admin panel posts route
adminPanelPostsBlueprint = Blueprint("adminPanelPosts", __name__)


@adminPanelPostsBlueprint.route("/admin/posts", methods=["GET", "POST"])
@adminPanelPostsBlueprint.route("/adminpanel/posts", methods=["GET", "POST"])
def adminPanelPosts():
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
                    # Check if the post delete button is clicked
                    match "postDeleteButton" in request.form:
                        case True:
                            # Delete the post from the database
                            deletePost(request.form["postID"])
            # Check if the user role is admin
            match role == "admin":
                case True:
                    # Connect to the posts database and get all the posts
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute("select * from posts order by timeStamp desc")
                    posts = cursor.fetchall()
                    # Render the dashboard template with the posts data and showPosts flag
                    return render_template(
                        "dashboard.html.jinja", posts=posts, showPosts=True
                    )
                case False:
                    # Redirect to the home page
                    return redirect("/")
        case False:
            # Redirect to the login page
            return redirect("/")
