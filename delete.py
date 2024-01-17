from helpers import (
    flash,
    sqlite3,
    message,
    session,
    redirect,
    DB_POSTS_ROOT,
    DB_USERS_ROOT,
    DB_COMMENTS_ROOT,
)


def deletePost(postID):
    connection = sqlite3.connect(DB_POSTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select author from posts where id = ? """,
        [(postID)],
    )
    cursor.execute(
        """delete from posts where id = ? """,
        [(postID)],
    )
    cursor.execute("update sqlite_sequence set seq = seq-1")
    connection.commit()
    connection.close()
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select count(*) from comments where post = ? """,
        [(postID)],
    )
    commentCount = list(cursor)[0][0]
    cursor.execute(
        """delete from comments where post = ? """,
        [(postID)],
    )
    cursor.execute(
        """update sqlite_sequence set seq = seq - ? """,
        [(commentCount)],
    )
    connection.commit()
    flash("post deleted", "error")
    message("2", f'POST: "{postID}" DELETED')


def deleteUser(userName):
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select * from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    cursor.execute(
        """select role from users where userName = ? """,
        [(session["userName"])],
    )
    perpetrator = cursor.fetchone()
    cursor.execute(
        """delete from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    cursor.execute("update sqlite_sequence set seq = seq-1")
    connection.commit()
    flash(f"user: {userName} deleted", "error")
    message("2", f'USER: "{userName}" DELETED')
    match perpetrator[0] == "admin":
        case True:
            return redirect(f"/admin/users")
        case False:
            session.clear()
            return redirect(f"/")


def deleteComment(commentID):
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select user from comments where id = ? """,
        [(commentID)],
    )
    cursor.execute(
        """delete from comments where id = ? """,
        [(commentID)],
    )
    cursor.execute("update sqlite_sequence set seq = seq-1")
    connection.commit()
    flash("comment deleted", "error")
    message("2", f'COMMENT: "{commentID}" DELETED')
