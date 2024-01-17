from helpers import message

message("3", "APP IS STARTING...")


from helpers import (
    render_template,
    getProfilePicture,
    Flask,
)


from routes.post import postBlueprint
from routes.user import userBlueprint
from routes.index import indexBlueprint
from routes.login import loginBlueprint
from routes.signup import signUpBlueprint
from routes.logout import logoutBlueprint
from routes.search import searchBlueprint
from routes.editPost import editPostBlueprint
from routes.searchBar import searchBarBlueprint
from routes.dashboard import dashboardBlueprint
from routes.verifyUser import verifyUserBlueprint
from routes.adminPanel import adminPanelBlueprint
from routes.createPost import createPostBlueprint
from routes.setUserRole import setUserRoleBlueprint
from routes.passwordReset import passwordResetBlueprint
from routes.changeUserName import changeUserNameBlueprint
from routes.changePassword import changePasswordBlueprint
from routes.adminPanelUsers import adminPanelUsersBlueprint
from routes.adminPanelPosts import adminPanelPostsBlueprint
from routes.accountSettings import accountSettingsBlueprint
from routes.adminPanelComments import adminPanelCommentsBlueprint
from routes.changeProfilePicture import changeProfilePictureBlueprint


from flask_wtf.csrf import CSRFProtect, CSRFError
from dbChecker import dbFolder, usersTable, postsTable, commentsTable

from constants import (
    LOG_IN,
    APP_HOST,
    APP_NAME,
    DEBUG_MODE,
    TAILWIND_UI,
    REGISTRATION,
    LOG_FILE_ROOT,
    APP_ROOT_PATH,
    APP_SECRET_KEY,
    SESSION_PERMANENT,
    APP_PORT,
)

from UISelector import TEMPLATE_FOLDER, STATIC_FOLDER

app = Flask(
    import_name=APP_NAME,
    root_path=APP_ROOT_PATH,
    static_folder=STATIC_FOLDER,
    template_folder=TEMPLATE_FOLDER,
)

app.secret_key = APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = SESSION_PERMANENT
csrf = CSRFProtect(app)

message("1", f"APP DEBUG MODE: {DEBUG_MODE}")
message("3", f"APP NAME: {APP_NAME}")
message("3", f"APP HOST: {APP_HOST}")
message("3", f"APP PORT: {APP_PORT}")
message("3", f"APP SECRET KEY: {APP_SECRET_KEY}")
message("3", f"APP SESSION PERMANENT: {SESSION_PERMANENT}")
message("3", f"APP ROOT PATH: {APP_ROOT_PATH}")
message("3", f"LOG FILE ROOT: {LOG_FILE_ROOT}")
message("3", f"LOG IN: {LOG_IN}")
message("3", f"REGISTRATION: {REGISTRATION}")


match TAILWIND_UI:
    case True:
        message("4", f"UI MODE: TAILWIND-CSS")
    case False:
        message("4", f"UI MODE: STANDARD-CSS")

message("4", f"TEMPLATE FOLDER: {TEMPLATE_FOLDER}")
message("4", f"STATIC FOLDER: {STATIC_FOLDER}")

dbFolder()
usersTable()
postsTable()
commentsTable()


@app.context_processor
def utility_processor():
    getProfilePicture
    return dict(getProfilePicture=getProfilePicture)


@app.errorhandler(404)
def notFound(e):
    return render_template("404.html"), 404


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    message("1", "CSRF ERROR")
    return render_template("csrfError.html", reason=e.description), 400


app.register_blueprint(postBlueprint)
app.register_blueprint(userBlueprint)
app.register_blueprint(indexBlueprint)
app.register_blueprint(loginBlueprint)
app.register_blueprint(signUpBlueprint)
app.register_blueprint(logoutBlueprint)
app.register_blueprint(searchBlueprint)
app.register_blueprint(editPostBlueprint)
app.register_blueprint(dashboardBlueprint)
app.register_blueprint(searchBarBlueprint)
app.register_blueprint(adminPanelBlueprint)
app.register_blueprint(createPostBlueprint)
app.register_blueprint(verifyUserBlueprint)
app.register_blueprint(setUserRoleBlueprint)
app.register_blueprint(passwordResetBlueprint)
app.register_blueprint(changeUserNameBlueprint)
app.register_blueprint(changePasswordBlueprint)
app.register_blueprint(adminPanelUsersBlueprint)
app.register_blueprint(adminPanelPostsBlueprint)
app.register_blueprint(accountSettingsBlueprint)
app.register_blueprint(adminPanelCommentsBlueprint)
app.register_blueprint(changeProfilePictureBlueprint)


match __name__:
    case "__main__":
        message("2", "APP STARTED SUCCESSFULLY")
        message("2", f"RUNNING ON http://{APP_HOST}:{APP_PORT}")
        app.run(debug=DEBUG_MODE, host=APP_HOST, port=APP_PORT)
        message("1", "APP SHUT DOWN")
