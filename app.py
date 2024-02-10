"""
This file contains the main function
"""

from modules import (
    Log,  # Importing the Log class for logging
    timedelta,  # Importing the timedelta class for working with time differences
    terminalASCII,  # Importing the terminalASCII function for displaying ASCII art in the terminal
    currentTimeStamp,  # Importing the currentTimeStamp function for getting the current timestamp
)


# Get the start time of the app
startTime = currentTimeStamp()

# Print a line breaker and a ASCII art
Log.breaker()
print(terminalASCII())

# Print a line breaker and a message that the app is starting
Log.app("STARTING...")


# Importing necessary modules and classes
from modules import (
    Flask,
)  # Importing Flask class for creating the Flask application instance

# Importing blueprints for different routes
from routes.post import postBlueprint  # Importing the blueprint for post route
from routes.user import userBlueprint  # Importing the blueprint for user route
from routes.index import (
    indexBlueprint,
)  # Importing the blueprint for index route
from routes.login import (
    loginBlueprint,
)  # Importing the blueprint for login route
from routes.about import (
    aboutBlueprint,
)  # Importing the blueprint for about route
from routes.signup import (
    signUpBlueprint,
)  # Importing the blueprint for signup route
from routes.logout import (
    logoutBlueprint,
)  # Importing the blueprint for logout route
from routes.search import (
    searchBlueprint,
)  # Importing the blueprint for search route
from routes.category import (
    categoryBlueprint,
)  # Importing the blueprint for category route
from routes.editPost import (
    editPostBlueprint,
)  # Importing the blueprint for post editing route
from routes.searchBar import (
    searchBarBlueprint,
)  # Importing the blueprint for search bar route
from routes.dashboard import (
    dashboardBlueprint,
)  # Importing the blueprint for dashboard route
from routes.verifyUser import (
    verifyUserBlueprint,
)  # Importing the blueprint for user verification route
from routes.adminPanel import (
    adminPanelBlueprint,
)  # Importing the blueprint for admin panel route
from routes.createPost import (
    createPostBlueprint,
)  # Importing the blueprint for creating post route
from routes.privacyPolicy import (
    privacyPolicyBlueprint,
)  # Importing the blueprint for privacy policy route
from routes.passwordReset import (
    passwordResetBlueprint,
)  # Importing the blueprint for password reset route
from routes.changeUserName import (
    changeUserNameBlueprint,
)  # Importing the blueprint for changing username route
from routes.changePassword import (
    changePasswordBlueprint,
)  # Importing the blueprint for changing password route
from routes.adminPanelUsers import (
    adminPanelUsersBlueprint,
)  # Importing the blueprint for admin panel users route
from routes.adminPanelPosts import (
    adminPanelPostsBlueprint,
)  # Importing the blueprint for admin panel posts route
from routes.accountSettings import (
    accountSettingsBlueprint,
)  # Importing the blueprint for account settings route
from routes.returnPostBanner import (
    returnPostBannerBlueprint,
)  # Importing the blueprint for returning post banners
from routes.adminPanelComments import (
    adminPanelCommentsBlueprint,
)  # Importing the blueprint for admin panel comments route
from routes.changeProfilePicture import (
    changeProfilePictureBlueprint,
)  # Importing the blueprint for changing profile picture route

from flask_wtf.csrf import (
    CSRFProtect,
    CSRFError,
)  # Importing CSRF protection for Flask forms

# Importing database related utilities
from utils.dbChecker import dbFolder, usersTable, postsTable, commentsTable

# Importing various configuration variables from the modules
from modules import (
    LOG_IN,  # Importing the log-in configuration
    UI_NAME,  # Importing the UI name configuration
    APP_HOST,  # Importing the application host configuration
    APP_NAME,  # Importing the application name configuration
    APP_PORT,  # Importing the application port configuration
    SMTP_MAIL,  # Importing the SMTP mail configuration
    SMTP_PORT,  # Importing the SMTP port configuration
    DEBUG_MODE,  # Importing the debug mode configuration
    APP_VERSION,  # Importing the application version configuration
    SMTP_SERVER,  # Importing the SMTP server configuration
    REGISTRATION,  # Importing the registration configuration
    SMTP_PASSWORD,  # Importing the SMTP password configuration
    DEFAULT_ADMIN,  # Importing the default admin configuration
    LOG_FILE_ROOT,  # Importing the log file root configuration
    APP_ROOT_PATH,  # Importing the application root path configuration
    STATIC_FOLDER,  # Importing the static folder configuration
    APP_SECRET_KEY,  # Importing the application secret key configuration
    RECAPTCHA_BADGE,  # Flag for enabling/disabling Recaptcha for badge configuration
    TEMPLATE_FOLDER,  # Importing the template folder configuration
    SESSION_PERMANENT,  # Importing the session permanence configuration
    DEFAULT_ADMIN_POINT,  # Importing the default admin point configuration
    DEFAULT_ADMIN_EMAIL,  # Importing the default admin email configuration
    DEFAULT_ADMIN_USERNAME,  # Importing the default admin username configuration
    DEFAULT_ADMIN_PASSWORD,  # Importing the default admin password configuration
    DEFAULT_ADMIN_PROFILE_PICTURE,  # Importing the default admin profile picture configuration
)

# Importing reCAPTCHA configurations
from modules import (
    RECAPTCHA,  # Flag for enabling/disabling Recaptcha
    RECAPTCHA_LOGIN,  # Flag for enabling/disabling Recaptcha for login
    RECAPTCHA_COMMENT,  # Flag for enabling/disabling Recaptcha for comment
    RECAPTCHA_SIGN_UP,  # Flag for enabling/disabling Recaptcha for sign-up
    RECAPTCHA_SITE_KEY,  # Flag for enabling/disabling Recaptcha for site key
    RECAPTCHA_POST_EDIT,  # Flag for enabling/disabling Recaptcha for post edit
    RECAPTCHA_SECRET_KEY,  # Flag for enabling/disabling Recaptcha for secret key
    RECAPTCHA_VERIFY_URL,  # Flag for enabling/disabling Recaptcha for verify URL
    RECAPTCHA_DELETE_USER,  # Flag for enabling/disabling Recaptcha for delete user
    RECAPTCHA_POST_DELETE,  # Flag for enabling/disabling Recaptcha for post delete
    RECAPTCHA_VERIFY_USER,  # Flag for enabling/disabling Recaptcha for verify user
    RECAPTCHA_POST_CREATE,  # Flag for enabling/disabling Recaptcha for post create
    RECAPTCHA_COMMENT_DELETE,  # Flag for enabling/disabling Recaptcha for comment delete
    RECAPTCHA_PASSWORD_RESET,  # Flag for enabling/disabling Recaptcha for password reset
    RECAPTCHA_PASSWORD_CHANGE,  # Flag for enabling/disabling Recaptcha for password change
    RECAPTCHA_USERNAME_CHANGE,  # Flag for enabling/disabling Recaptcha for username change
    RECAPTCHA_PROFILE_PICTURE_CHANGE,  # Flag for enabling/disabling Recaptcha for profile picture change
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


# Registering blueprints for different routes with the Flask application instance
app.register_blueprint(
    postBlueprint
)  # Registering the blueprint for handling post routes
app.register_blueprint(
    userBlueprint
)  # Registering the blueprint for handling user routes
app.register_blueprint(indexBlueprint)  # Registering the blueprint for the index route
app.register_blueprint(aboutBlueprint)  # Registering the blueprint for the about route
app.register_blueprint(loginBlueprint)  # Registering the blueprint for the login route
app.register_blueprint(
    signUpBlueprint
)  # Registering the blueprint for the sign-up route
app.register_blueprint(
    logoutBlueprint
)  # Registering the blueprint for the logout route
app.register_blueprint(
    searchBlueprint
)  # Registering the blueprint for the search route
app.register_blueprint(
    categoryBlueprint
)  # Registering the blueprint for the category route
app.register_blueprint(
    editPostBlueprint
)  # Registering the blueprint for the edit post route
app.register_blueprint(
    dashboardBlueprint
)  # Registering the blueprint for the dashboard route
app.register_blueprint(
    searchBarBlueprint
)  # Registering the blueprint for the search bar route
app.register_blueprint(
    adminPanelBlueprint
)  # Registering the blueprint for the admin panel route
app.register_blueprint(
    createPostBlueprint
)  # Registering the blueprint for the create post route
app.register_blueprint(
    verifyUserBlueprint
)  # Registering the blueprint for the verify user route
app.register_blueprint(
    privacyPolicyBlueprint
)  # Registering the blueprint for the privacy policy route
app.register_blueprint(
    passwordResetBlueprint
)  # Registering the blueprint for the password reset route
app.register_blueprint(
    changeUserNameBlueprint
)  # Registering the blueprint for the change username route
app.register_blueprint(
    changePasswordBlueprint
)  # Registering the blueprint for the change password route
app.register_blueprint(
    adminPanelUsersBlueprint
)  # Registering the blueprint for the admin panel users route
app.register_blueprint(
    adminPanelPostsBlueprint
)  # Registering the blueprint for the admin panel posts route
app.register_blueprint(
    accountSettingsBlueprint
)  # Registering the blueprint for the account settings route
app.register_blueprint(
    returnPostBannerBlueprint
)  # Registering the blueprint for the return post banner route
app.register_blueprint(
    adminPanelCommentsBlueprint
)  # Registering the blueprint for the admin panel comments route
app.register_blueprint(
    changeProfilePictureBlueprint
)  # Registering the blueprint for the change profile picture route


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
