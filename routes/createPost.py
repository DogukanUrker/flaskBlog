# Import the necessary modules and functions
from helpers import (
    flash,
    abort,
    session,
    sqlite3,
    request,
    message,
    redirect,
    addPoints,
    Blueprint,
    RECAPTCHA,
    requestsPost,
    DB_POSTS_ROOT,
    createPostForm,
    render_template,
    currentTimeStamp,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_POST_CREATE,
)

# Create a blueprint for the create post route
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
    match "userName" in session:
        case True:
            form = createPostForm(request.form)
            match request.method == "POST":
                case True:
                    postTitle = request.form["postTitle"]
                    postTags = request.form["postTags"]
                    postContent = request.form["postContent"]
                    postBanner = request.files["postBanner"].read()
                    postCategory = request.form["postCategory"]
                    match postContent == "":
                        case True:
                            flash("post content not be empty", "error")
                            message(
                                "1",
                                f'POST CONTENT NOT BE EMPTY USER: "{session["userName"]}"',
                            )
                        case False:
                                match RECAPTCHA and RECAPTCHA_POST_CREATE:
                                    case True:
                                        secretResponse = request.form[
                                                            "g-recaptcha-response"
                                                        ]
                                        verifyResponse = requestsPost(
                                                            url=f"{RECAPTCHA_VERIFY_URL}?secret={RECAPTCHA_SECRET_KEY}&response={secretResponse}"
                                                        ).json()
                                        match verifyResponse[
                                                            "success"
                                                        ] == True or verifyResponse[
                                                            "score"
                                                        ] > 0.5:
                                            case True:
                                                message("2",f"POST CREATE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                connection = sqlite3.connect(DB_POSTS_ROOT)
                                                cursor = connection.cursor()
                                                cursor.execute(
                                                    "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category) \
                                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                    (
                                                        postTitle,
                                                        postTags,
                                                        postContent,
                                                        postBanner,
                                                        session["userName"],
                                                        0,
                                                        currentTimeStamp(),
                                                        currentTimeStamp(),
                                                        postCategory
                                                    ),
                                                )
                                                connection.commit()
                                                message("2", f'POST: "{postTitle}" POSTED')
                                                addPoints(20, session["userName"])
                                                flash("You earned 20 points by posting ", "success")
                                                return redirect("/")
                                            case False:
                                                  message("1",f"POST CREATE RECAPTCHA | VERIFICATION: {verifyResponse["success"]} | VERIFICATION SCORE: {verifyResponse["score"]}")
                                                  abort(401)
                                    case False:
                                            connection = sqlite3.connect(DB_POSTS_ROOT)
                                            cursor = connection.cursor()
                                            cursor.execute(
                                                    "insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category) \
                                                    values(?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                                    (
                                                        postTitle,
                                                        postTags,
                                                        postContent,
                                                        postBanner,
                                                        session["userName"],
                                                        0,
                                                        currentTimeStamp(),
                                                        currentTimeStamp(),
                                                        postCategory
                                                    ),
                                                )
                                            connection.commit()
                                            message("2", f'POST: "{postTitle}" POSTED')
                                            addPoints(20, session["userName"])
                                            flash("You earned 20 points by posting ", "success")
                                            return redirect("/") 
            return render_template("createPost.html", form=form, siteKey=RECAPTCHA_SITE_KEY, recaptcha=RECAPTCHA,)
        case False:
            message("1", "USER NOT LOGGED IN")
            flash("you need loin for create a post", "error")
            return redirect("/login/redirect=&createpost")
