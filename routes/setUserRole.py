from helpers import sqlite3, Blueprint, session, redirect,message

setUserRoleBlueprint = Blueprint("setUserRole", __name__)


@setUserRoleBlueprint.route("/setuserrole/<userName>/<newRole>")
def setUserRole(userName,newRole):
    match "userName" in session:
        case True:
            connection = sqlite3.connect("db/users.db")
            cursor = connection.cursor()
            cursor.execute(
                f'select role from users where userName = "{session["userName"]}"'
            )
            role = cursor.fetchone()[0]
            match role == "admin":
                case  True:
                    cursor.execute(f'update users set role = "{newRole}" where lower(userName) = "{userName.lower()}" ')
                    connection.commit()
                    message("2",f'ADMIN: "{session["userName"]}" CHANGED USER: "{userName}"s ROLE TO {newRole}')
                    return redirect("/admin/users")
                case False:
                     return redirect("/")    
        case False:
            return redirect("/")    