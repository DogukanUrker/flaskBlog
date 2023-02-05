from helpers import (
    session,
    redirect,
    render_template,
    Blueprint,
)

accountSettingsBlueprint = Blueprint("accountSettings", __name__)


@accountSettingsBlueprint.route("/accountsettings")
def accountSettings():
    match "userName" in session:
        case True:
            return render_template("accountSettings.html")
        case False:
            return redirect("/login/redirect=&accountsettings")
