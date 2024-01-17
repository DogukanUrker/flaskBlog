from helpers import (
    flash,
    url_for,
    request,
    session,
    sqlite3,
    message,
    redirect,
    Blueprint,
    DB_POSTS_ROOT,
    DB_COMMENTS_ROOT,
    render_template,
)
from delete import deletePost

dashboardBlueprint = Blueprint("dashboard", __name__)


@dashboardBlueprint.route("/dashboard/<userName>", methods=["GET", "POST"])
def dashboard(userName):
    match "userName" in session:
        case True:
            match session["userName"].lower() == userName.lower():
                case True:
                    match request.method == "POST":
                        case True:
                            match "postDeleteButton" in request.form:
                                case True:
                                    deletePost(request.form["postID"])
                                    return (
                                        redirect(
                                            url_for(
                                                "dashboard.dashboard", userName=userName
                                            )
                                        ),
                                        301,
                                    )
                    connection = sqlite3.connect(DB_POSTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select * from posts where author = ? """,
                        [(session["userName"])],
                    )
                    posts = cursor.fetchall()
                    connection = sqlite3.connect(DB_COMMENTS_ROOT)
                    cursor = connection.cursor()
                    cursor.execute(
                        """select * from comments where lower(user) = ? """,
                        [(userName.lower())],
                    )
                    comments = cursor.fetchall()
                    match posts:
                        case []:
                            showPosts = False
                        case _:
                            showPosts = True
                    match comments:
                        case []:
                            showComments = False
                        case _:
                            showComments = True
                    return render_template(
                        "/dashboard.html",
                        posts=posts,
                        comments=comments,
                        showPosts=showPosts,
                        showComments=showComments,
                    )
                case False:
                    message(
                        "1",
                        f'THIS IS DASHBOARD NOT BELONGS TO USER: "{session["userName"]}"',
                    )
                    return redirect(f'/dashboard/{session["userName"].lower()}')
        case False:
            message("1", "DASHBOARD CANNOT BE ACCESSED WITHOUT USER LOGIN")
            flash("you need login for reach to dashboard", "error")
            return redirect("/login/redirect=&dashboard&user")
