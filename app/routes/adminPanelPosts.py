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
    DB_POSTS_ROOT,
    RECAPTCHA,
    RECAPTCHA_POST_DELETE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.log import Log
from utils.delete import Delete
from utils.flashMessage import flashMessage

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
            Log.database(
                f"Connecting to '{DB_POSTS_ROOT}' database"
            )  # Log the database connection is started
            # Connect to the posts database and get all the posts
            connection = sqlite3.connect(DB_POSTS_ROOT)
            connection.set_trace_callback(
                Log.database
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
            Log.error(
                f"{request.remote_addr} tried to reach post admin panel being logged in"
            )  # Log a message that the user tried to reach admin panel without being logged in
            # Redirect to the login page if the user is not logged in
            return redirect("/")
