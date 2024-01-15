from helpers import (
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
    cursor.execute(f"select author from posts where id = {postID}")
    cursor.execute(f"delete from posts where id = {postID}")
    cursor.execute(f"update sqlite_sequence set seq = seq-1")
    connection.commit()
    connection.close()
    connection = sqlite3.connect(DB_COMMENTS_ROOT)
    cursor = connection.cursor()
    cursor.execute(f"select count(*) from comments where post = {postID}")
    commentCount = list(cursor)[0][0]
    cursor.execute(f"delete from comments where post = {postID}")
    cursor.execute(f"update sqlite_sequence set seq = seq - {commentCount}")
    connection.commit()
    message("2", f'POST: "{postID}" DELETED')


def deleteUser(userName):
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(f'select * from users where lower(userName) = "{userName.lower()}"')
    cursor.execute(f'select role from users where userName = "{session["userName"]}"')
    perpetrator = cursor.fetchone()
    cursor.execute(f'delete from users where lower(userName) = "{userName.lower()}"')
    cursor.execute(f"update sqlite_sequence set seq = seq-1")
    connection.commit()
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
    cursor.execute(f"select user from comments where id = {commentID}")
    cursor.execute(f"delete from comments where id = {commentID}")
    cursor.execute(f"update sqlite_sequence set seq = seq-1")
    connection.commit()
    message("2", f'COMMENT: "{commentID}" DELETED')
