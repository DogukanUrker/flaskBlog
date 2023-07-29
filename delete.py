from helpers import sqlite3, message, redirect, session


def deletePost(postID):
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute(f"select author from posts where id = {postID}")
    cursor.execute(f"delete from posts where id = {postID}")
    cursor.execute(f"update sqlite_sequence set seq = seq-1")
    connection.commit()
    message("2", f'POST: "{postID}" DELETED')


def deleteUser(userName):
    connection = sqlite3.connect("db/users.db")
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
    connection = sqlite3.connect("db/comments.db")
    cursor = connection.cursor()
    cursor.execute(f"select user from comments where id = {commentID}")
    cursor.execute(f"delete from comments where id = {commentID}")
    cursor.execute(f"update sqlite_sequence set seq = seq-1")
    connection.commit()
    message("2", f'COMMENT: "{commentID}" DELETED')
