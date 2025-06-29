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
from settings import (
    DB_POSTS_ROOT,
    RECAPTCHA,
    RECAPTCHA_POST_CREATE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
)
from utils.addPoints import addPoints
from utils.flashMessage import flashMessage
from utils.forms.CreatePostForm import CreatePostForm
from utils.generateUrlIdFromPost import generateurlID
from utils.log import Log
from utils.time import currentTimeStamp

createPostBlueprint = Blueprint("createPost", __name__)


@createPostBlueprint.route("/createpost", methods=["GET", "POST"])
def createPost():
    """
    This function creates a new post for the user.

    Args:
        request (Request): The request object from the user.

    Returns:
        Response: The response object with the HTML template for the create post page.

    Raises:
        401: If the user is not authenticated.
    """

    if "userName" in session:
        form = CreatePostForm(request.form)

        if request.method == "POST":
            postTitle = request.form["postTitle"]
            postTags = request.form["postTags"]
            postContent = request.form["postContent"]
            postBanner = request.files["postBanner"].read()
            postCategory = request.form["postCategory"]

            if postContent == "":
                flashMessage(
                    page="createPost",
                    message="empty",
                    category="error",
                    language=session["language"],
                )
                Log.error(
                    f'User: "{session["userName"]}" tried to create a post with empty content',
                )
            else:
                if RECAPTCHA and RECAPTCHA_POST_CREATE:
                    secretResponse = request.form["g-recaptcha-response"]
                    verifyResponse = requestsPost(
                        url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                    ).json()

                    if (
                        verifyResponse["success"] is True
                        or verifyResponse["score"] > 0.5
                    ):
                        Log.success(
                            f"Post create reCAPTCHA| verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                        )
                        Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")

                        connection = sqlite3.connect(DB_POSTS_ROOT)
                        connection.set_trace_callback(Log.database)
                        cursor = connection.cursor()
                        cursor.execute(
                            "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category,urlID) \
                                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                postTitle,
                                postTags,
                                postContent,
                                postBanner,
                                session["userName"],
                                0,
                                currentTimeStamp(),
                                currentTimeStamp(),
                                postCategory,
                                generateurlID(postTitle),
                            ),
                        )
                        connection.commit()
                        Log.success(
                            f'Post: "{postTitle}" posted by "{session["userName"]}"',
                        )

                        addPoints(20, session["userName"])
                        flashMessage(
                            page="createPost",
                            message="success",
                            category="success",
                            language=session["language"],
                        )
                        return redirect("/")
                    else:
                        Log.error(
                            f"Post create reCAPTCHA | verification: {verifyResponse['success']} | verification score: {verifyResponse['score']}",
                        )
                        abort(401)
                else:
                    Log.database(f"Connecting to '{DB_POSTS_ROOT}' database")
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    connection.set_trace_callback(Log.database)
                    cursor = connection.cursor()
                    cursor.execute(
                        "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category,urlID) \
                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            postTitle,
                            postTags,
                            postContent,
                            postBanner,
                            session["userName"],
                            0,
                            currentTimeStamp(),
                            currentTimeStamp(),
                            postCategory,
                            generateurlID(),
                        ),
                    )
                    connection.commit()
                    Log.success(
                        f'Post: "{postTitle}" posted by "{session["userName"]}"',
                    )

                    addPoints(20, session["userName"])
                    flashMessage(
                        page="createPost",
                        message="success",
                        category="success",
                        language=session["language"],
                    )
                    return redirect("/")

        return render_template(
            "createPost.html.jinja",
            form=form,
            siteKey=RECAPTCHA_SITE_KEY,
            recaptcha=RECAPTCHA,
        )
    else:
        Log.error(f"{request.remote_addr} tried to create a new post without login")
        flashMessage(
            page="createPost",
            message="login",
            category="error",
            language=session["language"],
        )
        return redirect("/login/redirect=&createpost")
