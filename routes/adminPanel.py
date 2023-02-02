from helpers import sqlite3, render_template, Blueprint, session, redirect

adminPanelBlueprint = Blueprint("adminPanel", __name__)


@adminPanelBlueprint.route("/admin")
def adminPanel():
    match "userName" in session:
        case True:
            return render_template("adminPanel.html")
        case False:
            return redirect("/")
