"""
This file contains the blueprint for the logout page.

The functions and methods used in this blueprint are imported from the helpers module.
"""

from helpers import flash, message, Blueprint, session, redirect


logoutBlueprint = Blueprint("logout", __name__)


@logoutBlueprint.route("/logout")
def logout():
    """
    This function handles the logout process.

    It checks if the user is logged in. If they are, their session is cleared and they are redirected
    to the homepage. A message is also displayed indicating that the user has been logged out.

    If the user is not logged in, a message is displayed indicating that they are not logged in.
    The user is then redirected to the homepage.
    """
    if "userName" in session:
        message("2", f"USER: {session['userName']} LOGGED OUT")
        session.clear()
        flash("logged out", "error")
        return redirect("/")
    else:
        message("1", "USER NOT LOGGED IN")
        return redirect("/")
