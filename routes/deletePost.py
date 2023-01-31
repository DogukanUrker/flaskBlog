from helpers import (
    session,
    sqlite3,
    message,
    redirect,
    Blueprint,
)

deletePostBlueprint = Blueprint("deletePost", __name__)


@deletePostBlueprint.route("/deletepost/<int:postID>/redirect=<direct>")
def deletePost(postID, direct):
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/posts.db")
            cursor = connection.cursor()
            cursor.execute(f"select author from posts where id = {postID}")
            author = cursor.fetchone()
            direct = direct.replace("&", "/")
            match author[0] == session["userName"]:
                case True:
                    cursor.execute(f"delete from posts where id = {postID}")
                    cursor.execute(f"update sqlite_sequence set seq = seq-1")
                    connection.commit()
                    message("2", f'POST: "{postID}" DELETED')
                    return redirect(f"/{direct}")
                case False:
                    message(
                        "1",
                        f'POST: "{postID}" NOT DELETED "{postID}" DOES NOT BELONG TO USER: {session["userName"]}',
                    )
                    return redirect(f"/{direct}")
            return redirect(f"/{direct}")
        case False:
            message("1", f'USER NEEDS TO LOGIN FOR DELETE POST: "{postID}"')
            return redirect(f"/{direct}")
