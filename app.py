"""
This file contains the main function
"""
# Import the message function from the helpers module
from helpers import message

# Print a line breaker and a message that the app is starting
message(breaker=True)
message("3", "APP IS STARTING...")


# Import other functions and modules from the helpers module
from helpers import (
    render_template,
    getProfilePicture,
    Flask,
)


# Import the blueprints for the different routes from the routes module
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
from routes.passwordReset import passwordResetBlueprint
from routes.changeUserName import changeUserNameBlueprint
from routes.changePassword import changePasswordBlueprint
from routes.adminPanelUsers import adminPanelUsersBlueprint
from routes.adminPanelPosts import adminPanelPostsBlueprint
from routes.accountSettings import accountSettingsBlueprint
from routes.adminPanelComments import adminPanelCommentsBlueprint
from routes.changeProfilePicture import changeProfilePictureBlueprint

# Import the CSRFProtect and CSRFError classes from the flask_wtf.csrf module
from flask_wtf.csrf import CSRFProtect, CSRFError

# Import the dbFolder, usersTable, postsTable and commentsTable functions from the dbChecker module
from dbChecker import dbFolder, usersTable, postsTable, commentsTable

# Import the constants from the constants module
from constants import (
    LOG_IN,
    APP_HOST,
    APP_NAME,
    APP_PORT,
    DEBUG_MODE,
    TAILWIND_UI,
    REGISTRATION,
    LOG_FILE_ROOT,
    APP_ROOT_PATH,
    APP_SECRET_KEY,
    RECAPTCHA_BADGE,
    SESSION_PERMANENT,
)

# Import the recaptcha-related variables from the helpers module
from helpers import (
    RECAPTCHA,
    RECAPTCHA_LOGIN,
    RECAPTCHA_COMMENT,
    RECAPTCHA_SIGN_UP,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_POST_EDIT,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_DELETE_USER,
    RECAPTCHA_POST_DELETE,
    RECAPTCHA_VERIFY_USER,
    RECAPTCHA_POST_CREATE,
    RECAPTCHA_COMMENT_DELETE,
    RECAPTCHA_PASSWORD_RESET,
    RECAPTCHA_PASSWORD_CHANGE,
    RECAPTCHA_USERNAME_CHANGE,
    RECAPTCHA_PROFILE_PICTURE_CHANGE,
)

# Check if the TAILWIND_UI flag is True
match TAILWIND_UI:
    case True:
        # Set the template folder and the static folder to the tailwindUI subfolders
        TEMPLATE_FOLDER = "templates/tailwindUI"
        STATIC_FOLDER = "static/tailwindUI"
    case False:
        # Set the template folder and the static folder to the standardUI subfolders
        TEMPLATE_FOLDER = "templates/standardUI"
        STATIC_FOLDER = "static/standardUI"

# Create a Flask app object with the app name, root path, static folder and template folder
app = Flask(
    import_name=APP_NAME,
    root_path=APP_ROOT_PATH,
    static_folder=STATIC_FOLDER,
    template_folder=TEMPLATE_FOLDER,
)

# Set the secret key and the session permanent flag for the app
app.secret_key = APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = SESSION_PERMANENT

# Create a CSRFProtect object for the app
csrf = CSRFProtect(app)


# Print a line breaker and a message that the app is starting
message(breaker=True)
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
message(breaker=True)


# Check if recaptcha is enabled
match RECAPTCHA:
    case True:
        # Check if the recaptcha site key and secret key are valid
        match RECAPTCHA_SITE_KEY == "" or RECAPTCHA_SECRET_KEY == "":
            case True:
                # Log a warning message that the recaptcha keys are invalid and may cause the app to crash
                message(
                    "1",
                    f"RECAPTCHA KEYS IS UNVALID THIS MAY CAUSE THE APPLICATION TO CRASH",
                )
                message(
                    "1",
                    f"PLEASE CHECK YOUR RECAPTCHA KEYS OR SET RECAPTCHA TO FALSE FROM TRUE IN 'constants.py'",
                )
            case False:
                # Log a success message that recaptcha is on and print the recaptcha keys, url and badge status
                message("2", "RECAPTCHA IS ON")
                message("3", f"RECAPTCHA RECAPTCHA_SITE_KEY KEY: {RECAPTCHA_SITE_KEY}")
                message("3", f"RECAPTCHA SECRET KEY: {RECAPTCHA_SECRET_KEY}")
                message("3", f"RECAPTCHA VERIFY URL: {RECAPTCHA_VERIFY_URL}")
                message("3", f"RECAPTCHA BADGE: {RECAPTCHA_BADGE}")
                # Log the recaptcha settings for different actions
                message("6", f"RECAPTCHA LOGIN: {RECAPTCHA_LOGIN}")
                message("6", f"RECAPTCHA SIGN UP: {RECAPTCHA_SIGN_UP }")
                message("6", f"RECAPTCHA POST CREATE: {RECAPTCHA_POST_CREATE}")
                message("6", f"RECAPTCHA POST EDIT: {RECAPTCHA_POST_EDIT }")
                message("6", f"RECAPTCHA POST DELETE: {RECAPTCHA_POST_DELETE}")
                message("6", f"RECAPTCHA COMMENT: {RECAPTCHA_COMMENT}")
                message("6", f"RECAPTCHA COMMENT DELETE: {RECAPTCHA_COMMENT_DELETE}")
                message("6", f"RECAPTCHA PASSWORD RESET: {RECAPTCHA_PASSWORD_RESET}")
                message("6", f"RECAPTCHA PASSWORD CHANGE: {RECAPTCHA_PASSWORD_CHANGE}")
                message("6", f"RECAPTCHA USERNAME CHANGE: {RECAPTCHA_USERNAME_CHANGE}")
                message("6", f"RECAPTCHA VERIFY USER: {RECAPTCHA_VERIFY_USER}")
                message("6", f"RECAPTCHA DELETE USER: {RECAPTCHA_DELETE_USER}")
                message(
                    "6",
                    f"RECAPTCHA USER PROFILE PICTURE CHANGE: {RECAPTCHA_PROFILE_PICTURE_CHANGE}",
                )
                message(
                    "6",
                    f"RECAPTCHA PROFILE PICTURE CHANGE: {RECAPTCHA_PROFILE_PICTURE_CHANGE}",
                )
    case False:
        # Log a warning message that recaptcha is off
        message("1", f"RECAPTCHA IS OFF")
message(breaker=True)
# Check if the tailwind UI flag is True
match TAILWIND_UI:
    case True:
        # Log a message that the UI mode is tailwind-css and set the template folder and the static folder accordingly
        message("4", f"UI MODE: TAILWIND-CSS")
        TEMPLATE_FOLDER = "templates/tailwindUI"
        STATIC_FOLDER = "static/tailwindUI"
    case False:
        # Log a message that the UI mode is standard-css and set the template folder and the static folder accordingly
        message("4", f"UI MODE: STANDARD-CSS")
        TEMPLATE_FOLDER = "templates/standardUI"
        STATIC_FOLDER = "static/standardUI"

# Log the template folder and the static folder
message("4", f"TEMPLATE FOLDER: {TEMPLATE_FOLDER}")
message("4", f"STATIC FOLDER: {STATIC_FOLDER}")

message(breaker=True)
# Call the dbFolder, usersTable, postsTable and commentsTable functions to check the database status
dbFolder()
usersTable()
postsTable()
commentsTable()
message(breaker=True)


# Define a context processor function for the app
@app.context_processor
def returnUserProfilePicture():
    # Return a dictionary with the getProfilePicture function as a value
    getProfilePicture
    return dict(getProfilePicture=getProfilePicture)


# Define a context processor function for the app
@app.context_processor
def recaptchaBadge():
    # This function checks the recaptcha and recaptcha badge values. If values are both True, then returns True
    def recaptchaBadge():
        match RECAPTCHA and RECAPTCHA_BADGE:
            case True:
                return True
            case False:
                return False

    # Return a dictionary with the recaptchaBadge function as a value
    return dict(recaptchaBadge=recaptchaBadge())


# Define an error handler function for the 404 error
@app.errorhandler(404)
def notFound(e):
    # Render the 404 template and return a 404 status code
    return render_template("404.html"), 404


# Define an error handler function for the 401 error
@app.errorhandler(401)
def unauthorized(e):
    # Log a message that a 401 unauthorized error occurred
    message("1", "401 UNAUTHORIZED ERROR")
    # Render the 401 template and return a 401 status code
    return render_template("401.html"), 401


# Define an error handler function for the CSRFError
@app.errorhandler(CSRFError)
def csrfError(e):
    # Log a message that a CSRF error occurred
    message("1", "CSRF ERROR")
    # Render the csrfError template with the reason and return a 400 status code
    return render_template("csrfError.html", reason=e.description), 400


# Register the blueprints for the different routes with the app object
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
app.register_blueprint(passwordResetBlueprint)
app.register_blueprint(changeUserNameBlueprint)
app.register_blueprint(changePasswordBlueprint)
app.register_blueprint(adminPanelUsersBlueprint)
app.register_blueprint(adminPanelPostsBlueprint)
app.register_blueprint(accountSettingsBlueprint)
app.register_blueprint(adminPanelCommentsBlueprint)
app.register_blueprint(changeProfilePictureBlueprint)


# Check if the name of the module is the main module
match __name__:
    case "__main__":
        # Log a message that the app started successfully and print the host and port
        message("2", "APP STARTED SUCCESSFULLY")
        message("2", f"RUNNING ON http://{APP_HOST}:{APP_PORT}")
        message(breaker=True)
        # Run the app with the debug mode, host and port settings
        app.run(debug=DEBUG_MODE, host=APP_HOST, port=APP_PORT)
        message(breaker=True)
        # Log a message that the app shut down
        message("1", "APP SHUT DOWN")
