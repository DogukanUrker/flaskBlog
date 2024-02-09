"""
This file contains the main function
"""

# Import the log class from the modules module
from modules import Log, terminalASCII, currentTimeStamp, timedelta

# Get the start time of the app
startTime = currentTimeStamp()

# Print a line breaker and a ASCII art
Log.breaker()
print(terminalASCII())

# Print a line breaker and a message that the app is starting
Log.app("STARTING...")


# Import other functions and modules from the modules module
from modules import (
    Flask,
)


# Import the blueprints for the different routes from the routes module
from routes.post import postBlueprint
from routes.user import userBlueprint
from routes.index import indexBlueprint
from routes.login import loginBlueprint
from routes.about import aboutBlueprint
from routes.signup import signUpBlueprint
from routes.logout import logoutBlueprint
from routes.search import searchBlueprint
from routes.category import categoryBlueprint
from routes.editPost import editPostBlueprint
from routes.searchBar import searchBarBlueprint
from routes.dashboard import dashboardBlueprint
from routes.verifyUser import verifyUserBlueprint
from routes.adminPanel import adminPanelBlueprint
from routes.createPost import createPostBlueprint
from routes.privacyPolicy import privacyPolicyBlueprint
from routes.passwordReset import passwordResetBlueprint
from routes.changeUserName import changeUserNameBlueprint
from routes.changePassword import changePasswordBlueprint
from routes.adminPanelUsers import adminPanelUsersBlueprint
from routes.adminPanelPosts import adminPanelPostsBlueprint
from routes.accountSettings import accountSettingsBlueprint
from routes.returnPostBanner import returnPostBannerBlueprint
from routes.adminPanelComments import adminPanelCommentsBlueprint
from routes.changeProfilePicture import changeProfilePictureBlueprint

# Import the CSRFProtect and CSRFError classes from the flask_wtf.csrf module
from flask_wtf.csrf import CSRFProtect, CSRFError

# Import the dbFolder, usersTable, postsTable and commentsTable functions from the dbChecker module
from utils.dbChecker import dbFolder, usersTable, postsTable, commentsTable

# Import the constants from the constants module
from modules import (
    LOG_IN,
    UI_NAME,
    APP_HOST,
    APP_NAME,
    APP_PORT,
    SMTP_MAIL,
    SMTP_PORT,
    DEBUG_MODE,
    APP_VERSION,
    SMTP_SERVER,
    REGISTRATION,
    SMTP_PASSWORD,
    DEFAULT_ADMIN,
    LOG_FILE_ROOT,
    APP_ROOT_PATH,
    STATIC_FOLDER,
    APP_SECRET_KEY,
    RECAPTCHA_BADGE,
    TEMPLATE_FOLDER,
    SESSION_PERMANENT,
    DEFAULT_ADMIN_POINT,
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_PROFILE_PICTURE,
)

# Import the recaptcha-related variables from the modules module
from modules import (
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

from utils.errorHandlers.notFoundErrorHandler import (
    notFoundErrorHandler,
)  # This function handles 404 errors

from utils.errorHandlers.csrfErrorHandler import (
    csrfErrorHandler,
)  # This function handles CSRF errors

from utils.errorHandlers.unauthorizedErrorHandler import (
    unauthorizedErrorHandler,
)  # This function handles unauthorized access errors


# Import the contextProcessor module that contains custom functions for the app
from modules import (
    isLogin,  # A function that checks LOG_IN constant
    recaptchaBadge,  # A function that checks RECAPTCHA_BADGE constant
    isRegistration,  # A function that checks REGISTRATION constant
    returnUserProfilePicture,  # A function that returns the user's profile picture
)

# Create a Flask app object with the app name, root path, static folder and template folder
app = Flask(
    import_name=APP_NAME,  # The name of the app
    root_path=APP_ROOT_PATH,  # The root path of the app
    static_folder=STATIC_FOLDER,  # The folder where the static files(*.js/*.css) are stored
    template_folder=TEMPLATE_FOLDER,  # The folder where the Jinja(*.html.jinja) templates are stored
)

# Set the secret key and the session permanent flag for the app
app.secret_key = APP_SECRET_KEY  # The secret key for the app
app.config["SESSION_PERMANENT"] = (
    SESSION_PERMANENT  # A flag that determines if the session is permanent or not
)

# Create a CSRFProtect object for the app
csrf = CSRFProtect(app)  # A CSRF protection mechanism for the app

# Register the custom functions from the contextProcessor module as context processors for the app
# Context processors are functions that run before rendering a template and add variables to the template context
app.context_processor(
    isLogin
)  # A context processor that adds the isLogin variable to the template context
app.context_processor(
    recaptchaBadge
)  # A context processor that adds the recaptchaBadge variable to the template context
app.context_processor(
    isRegistration
)  # A context processor that adds the isRegistration variable to the template context
app.context_processor(
    returnUserProfilePicture
)  # A context processor that adds the getProfilePicture variable to the template context

# Log app settings
Log.app(f"DEBUG MODE: {DEBUG_MODE}")
Log.app(f"NAME: {APP_NAME}")
Log.app(f"VERSION: {APP_VERSION}")
Log.app(f"HOST: {APP_HOST}")
Log.app(f"PORT: {APP_PORT}")
Log.app(f"SECRET KEY: {APP_SECRET_KEY}")
Log.app(f"SESSION PERMANENT: {SESSION_PERMANENT}")
Log.app(f"ROOT PATH: {APP_ROOT_PATH}")
Log.app(f"LOG FILE ROOT: {LOG_FILE_ROOT}")
Log.app(f"LOG IN: {LOG_IN}")
Log.app(f"REGISTRATION: {REGISTRATION}")
# Log the UI name, template folder and the static folder
Log.app(f"UI: {UI_NAME}")
Log.app(f"TEMPLATE FOLDER: {TEMPLATE_FOLDER}")
Log.app(f"STATIC FOLDER: {STATIC_FOLDER}")
# Log the SMTP server settings
Log.app(f"SMTP SERVER: {SMTP_SERVER}")
Log.app(f"SMTP PORT: {SMTP_PORT}")
Log.app(f"SMTP MAIL: {SMTP_MAIL}")
Log.app(f"SMTP PASSWORD: {SMTP_PASSWORD}")

# Check if recaptcha is enabled
match RECAPTCHA:
    case True:
        # Check if the recaptcha site key and secret key are valid
        match RECAPTCHA_SITE_KEY == "" or RECAPTCHA_SECRET_KEY == "":
            case True:
                # Log a warning message that the recaptcha keys are invalid and may cause the app to crash
                Log.danger(
                    f"RECAPTCHA KEYS IS UNVALID THIS MAY CAUSE THE APPLICATION TO CRASH",
                )
                Log.danger(
                    f"PLEASE CHECK YOUR RECAPTCHA KEYS OR SET RECAPTCHA TO FALSE FROM TRUE IN 'constants.py'",
                )
            case False:
                # Log a success message that recaptcha is on and print the recaptcha keys, url and badge status
                Log.app("RECAPTCHA IS ON")
                Log.app(f"RECAPTCHA RECAPTCHA_SITE_KEY KEY: {RECAPTCHA_SITE_KEY}")
                Log.app(f"RECAPTCHA SECRET KEY: {RECAPTCHA_SECRET_KEY}")
                Log.app(f"RECAPTCHA VERIFY URL: {RECAPTCHA_VERIFY_URL}")
                Log.app(f"RECAPTCHA BADGE: {RECAPTCHA_BADGE}")
                # Log the recaptcha settings for different actions
                Log.app(f"RECAPTCHA LOGIN: {RECAPTCHA_LOGIN}")
                Log.app(f"RECAPTCHA SIGN UP: {RECAPTCHA_SIGN_UP }")
                Log.app(f"RECAPTCHA POST CREATE: {RECAPTCHA_POST_CREATE}")
                Log.app(f"RECAPTCHA POST EDIT: {RECAPTCHA_POST_EDIT }")
                Log.app(f"RECAPTCHA POST DELETE: {RECAPTCHA_POST_DELETE}")
                Log.app(f"RECAPTCHA COMMENT: {RECAPTCHA_COMMENT}")
                Log.app(f"RECAPTCHA COMMENT DELETE: {RECAPTCHA_COMMENT_DELETE}")
                Log.app(f"RECAPTCHA PASSWORD RESET: {RECAPTCHA_PASSWORD_RESET}")
                Log.app(f"RECAPTCHA PASSWORD CHANGE: {RECAPTCHA_PASSWORD_CHANGE}")
                Log.app(f"RECAPTCHA USERNAME CHANGE: {RECAPTCHA_USERNAME_CHANGE}")
                Log.app(f"RECAPTCHA VERIFY USER: {RECAPTCHA_VERIFY_USER}")
                Log.app(f"RECAPTCHA DELETE USER: {RECAPTCHA_DELETE_USER}")
                Log.app(
                    f"RECAPTCHA USER PROFILE PICTURE CHANGE: {RECAPTCHA_PROFILE_PICTURE_CHANGE}",
                )
                Log.app(
                    f"RECAPTCHA PROFILE PICTURE CHANGE: {RECAPTCHA_PROFILE_PICTURE_CHANGE}",
                )
    case False:
        # Log a warning message that recaptcha is off
        Log.app(f"RECAPTCHA IS OFF")

# Check if default admin is enabled
match DEFAULT_ADMIN:
    case True:
        # Log a success message that admin is on and print the default admin settings
        Log.app(f"DEFAULT ADMIN IS ON")
        Log.app(f"DEFAULT ADMIN USERNAME: {DEFAULT_ADMIN_USERNAME}")
        Log.app(f"DEFAULT ADMIN EMAIL: {DEFAULT_ADMIN_EMAIL}")
        Log.app(f"DEFAULT ADMIN PASSWORD: {DEFAULT_ADMIN_PASSWORD}")
        Log.app(f"DEFAULT ADMIN POINT: {DEFAULT_ADMIN_POINT}")
        Log.app(f"DEFAULT ADMIN PROFILE PICTURE: {DEFAULT_ADMIN_PROFILE_PICTURE}")
    case False:
        # Log a danger message that admin is off
        Log.app(f"DEFAULT ADMIN IS OFF")

# Call the dbFolder, usersTable, postsTable and commentsTable functions to check the database status
dbFolder()
usersTable()
postsTable()
commentsTable()


# Use the app.errorhandler decorator to register error handler functions for your app
@app.errorhandler(404)
def notFound(e):
    # Call the notFoundErrorHandler function and return its result
    return notFoundErrorHandler(e)


# Use the app.errorhandler decorator to register error handler functions for your app
@app.errorhandler(401)
def unauthorized(e):
    # Call the unauthorizedErrorHandler function and return its result
    return unauthorizedErrorHandler(e)


# Use the app.errorhandler decorator to register error handler functions for your app
@app.errorhandler(CSRFError)
def csrfError(e):
    # Call the csrfErrorHandler function and return its result
    return csrfErrorHandler(e)


# Register the blueprints for the different routes with the app object
app.register_blueprint(postBlueprint)
app.register_blueprint(userBlueprint)
app.register_blueprint(indexBlueprint)
app.register_blueprint(aboutBlueprint)
app.register_blueprint(loginBlueprint)
app.register_blueprint(signUpBlueprint)
app.register_blueprint(logoutBlueprint)
app.register_blueprint(searchBlueprint)
app.register_blueprint(categoryBlueprint)
app.register_blueprint(editPostBlueprint)
app.register_blueprint(dashboardBlueprint)
app.register_blueprint(searchBarBlueprint)
app.register_blueprint(adminPanelBlueprint)
app.register_blueprint(createPostBlueprint)
app.register_blueprint(verifyUserBlueprint)
app.register_blueprint(privacyPolicyBlueprint)
app.register_blueprint(passwordResetBlueprint)
app.register_blueprint(changeUserNameBlueprint)
app.register_blueprint(changePasswordBlueprint)
app.register_blueprint(adminPanelUsersBlueprint)
app.register_blueprint(adminPanelPostsBlueprint)
app.register_blueprint(accountSettingsBlueprint)
app.register_blueprint(returnPostBannerBlueprint)
app.register_blueprint(adminPanelCommentsBlueprint)
app.register_blueprint(changeProfilePictureBlueprint)


# Check if the name of the module is the main module
match __name__:
    case "__main__":
        # Log a message that the app started successfully and print the host and port
        Log.success("STARTED SUCCESSFULLY")
        Log.app(f"RUNNING ON http://{APP_HOST}:{APP_PORT}")

        # Print a ASCII art
        print(terminalASCII())

        # Run the app with the debug mode, host and port settings
        app.run(debug=DEBUG_MODE, host=APP_HOST, port=APP_PORT)

        # Get the end time of the app
        endTime = currentTimeStamp()

        # Calculate the run time of the app
        runTime = endTime - startTime

        # Convert the run time to a string
        runTime = str(timedelta(seconds=runTime))

        # Log a message that shows the run time of the app
        Log.app(f"RUN TIME: {runTime} ")

        # Log a message that the app shut down
        Log.app("SHUT DOWN")

        # Log a warning message that the app shut down
        Log.warning("APP SHUT DOWN")

        # Print a ASCII art
        print(terminalASCII())

        # Print a line breaker
        Log.breaker()
