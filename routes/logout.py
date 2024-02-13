"""
This file contains the blueprint for the logout page.

The functions and methods used in this blueprint are imported from the modules module.
"""

from modules import (
    Log,  # A function for logging messages
    flash,  # A function for displaying flash messages
    session,  # A dictionary for storing session data
    request,  # Module for handling HTTP requests
    redirect,  # A function for returning redirect responses
    Blueprint,  # A class for creating Flask blueprints
)


logoutBlueprint = Blueprint(
    "logout", __name__
)  # Create a blueprint for the logout route with the name "logout" and the current module name


@logoutBlueprint.route("/logout")  # Define a route for the logout page
def logout():
    """
    This function handles the logout process.

    It checks if the user is logged in. If they are, their session is cleared and they are redirected
    to the homepage. A message is also displayed indicating that the user has been logged out.

    If the user is not logged in, a message is displayed indicating that they are not logged in.
    The user is then redirected to the homepage.
    """
    match "userName" in session:  # Use a match statement to check if the "userName" key is present in the session dictionary
        case True:  # If the user is logged in
            Log.success(
                f"User: {session['userName']} logged out"
            )  # Log a message with level 2 indicating the user has logged out
            session.clear()  # Clear the session dictionary
            flash(
                "Logged out.", "error"
            )  # Display a flash message with the text "logged out" and the category "error"
            return redirect("/")  # Return a redirect response to the homepage
        case False:  # If the user is not logged in
            Log.danger(
                f"{request.remote_addr} tried to logout without being logged in"
            )  # Log a message with level 1 indicating the user is not logged in
            return redirect("/")  # Return a redirect response to the homepage
