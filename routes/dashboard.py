from helpers import (
    session,
    sqlite3,
    flash,
    message,
    redirect,
    render_template,
    Blueprint,
)

dashboardBlueprint = Blueprint("dashboard", __name__)


@dashboardBlueprint.route("/dashboard/<userName>")
def dashboard(userName):
    match "userName" in session:
        case True:
            match session["userName"].lower() == userName.lower():
                case True:
                    connection = sqlite3.connect("db/posts.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f'select * from posts where author = "{session["userName"]}"'
                    )
                    posts = cursor.fetchall()
                    connection = sqlite3.connect("db/comments.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f'select * from comments where lower(user) = "{userName.lower()}"'
                    )
                    comments = cursor.fetchall()
                    if posts:
                        showPosts = True
                    elif not posts:
                        showPosts = False
                    if comments:
                        showComments = True
                    elif not comments:
                        showComments = False
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
