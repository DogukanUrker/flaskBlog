# Import the necessary modules and functions
from helpers import (
    request,
    sqlite3,
    session,
    redirect,
    Blueprint,
    DB_USERS_ROOT,
    render_template,
    DB_COMMENTS_ROOT,
)
from delete import deleteComment

# Create a blueprint for the admin panel comments route
adminPanelCommentsBlueprint = Blueprint("adminPanelComments", __name__)


@adminPanelCommentsBlueprint.route("/admin/comments", methods=["GET", "POST"])
@adminPanelCommentsBlueprint.route("/adminpanel/comments", methods=["GET", "POST"])
def adminPanelComments():
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
                    # Check if the comment delete button is clicked
                    match "commentDeleteButton" in request.form:
                        case True:
                            # Delete the comment from the database
                            deleteComment(request.form["commentID"])
                    # Redirect to the same route
                    return redirect(f"/admin/comments")
            # Check if the user role is admin
            match role == "admin":
                case True:
                    # Connect to the comments database and get all the comments
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute("select * from comments order by timeStamp desc")
                    comments = cursor.fetchall()
                    # Render the admin panel comments template with the comments data
                    return render_template(
                        "adminPanelComments.html.jinja", comments=comments
                    )
                case False:
                    # Redirect to the home page
                    return redirect("/")
        case False:
            # Redirect to the login page
            return redirect("/")
