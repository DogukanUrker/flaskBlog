from helpers import (
    session,
    sqlite3,
    message,
    redirect,
    Blueprint,
)

deleteCommentBlueprint = Blueprint("deleteComment", __name__)


@deleteCommentBlueprint.route("/deletecomment/<int:commentID>/redirect=<direct>")
def deleteComment(commentID, direct):
    direct = direct.replace("&", "/")
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/comments.db")
            cursor = connection.cursor()
            cursor.execute(f"select user from comments where id = {commentID}")
            user = cursor.fetchone()
            match user[0] == session["userName"]:
                case True:
                    cursor.execute(f"delete from comments where id = {commentID}")
                    cursor.execute(f"update sqlite_sequence set seq = seq-1")
                    connection.commit()
                    message("2", f'COMMENT: "{commentID}" DELETED')
                    return redirect(f"/{direct}")
                case False:
                    message(
                        "1",
                        f'COMMENT: "{commentID}" NOT DELETED "{commentID}" DOES NOT BELONG TO {session["userName"]}',
                    )
                    return redirect(f"/{direct}")
        case False:
            message("1", f"USER NEEDS TO LOGIN FOR DELETE COMMENT: {commentID}")
            return redirect(f"/{direct}")
