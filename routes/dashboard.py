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
            match session["userName"].lower() == userName:
                case True:
                    connection = sqlite3.connect("db/posts.db")
                    cursor = connection.cursor()
                    cursor.execute(
                        f'select * from posts where author = "{session["userName"]}"'
                    )
                    posts = cursor.fetchall()
                    return render_template(
                        "/dashboard.html",
                        posts=posts,
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
            return redirect("/login")
