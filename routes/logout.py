from helpers import session, redirect, message, Blueprint


logoutBlueprint = Blueprint("logout", __name__)


@logoutBlueprint.route("/logout")
def logout():
    match "userName" in session:
        case True:
            message("2", f'USER: "{session["userName"]}" LOGGED OUT')
            session.clear()
            return redirect("/")
        case False:
            message("1", f"USER NOT LOGGED IN")
            return redirect("/")
