# Import necessary modules and functions
import sqlite3
from flask import (
    Blueprint,
    abort,
    redirect,
    render_template,
    request,
    session,
)
from requests import post as requestsPost
from constants import (
    DB_COMMENTS_ROOT,
    RECAPTCHA,
    RECAPTCHA_COMMENT_DELETE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.log import Log
from utils.delete import Delete
from utils.flashMessage import flashMessage

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
            Log.database(
                f"Connecting to '{DB_COMMENTS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the comments database and get all the comments
            connection = sqlite3.connect(DB_COMMENTS_ROOT)
            connection.set_trace_callback(
                Log.database
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
            Log.error(
                f"{request.remote_addr} tried to reach comment admin panel being logged in"
            )  # Log a message that the user tried to reach admin panel without being logged in
            # Redirect to the login page if the user is not logged in
            return redirect("/")
