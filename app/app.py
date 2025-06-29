"""
This file contains the main function
"""

from datetime import timedelta

from flask import Flask
from flask_wtf.csrf import (
    CSRFError,
    CSRFProtect,
)
from routes.about import (
    aboutBlueprint,
)
from routes.accountSettings import (
    accountSettingsBlueprint,
)
from routes.adminPanel import (
    adminPanelBlueprint,
)
from routes.adminPanelComments import (
    adminPanelCommentsBlueprint,
)
from routes.adminPanelPosts import (
    adminPanelPostsBlueprint,
)
from routes.adminPanelUsers import (
    adminPanelUsersBlueprint,
)
from routes.category import (
    categoryBlueprint,
)
from routes.changeLanguage import (
    changeLanguageBlueprint,
)
from routes.changePassword import (
    changePasswordBlueprint,
)
from routes.changeProfilePicture import (
    changeProfilePictureBlueprint,
)
from routes.changeUserName import (
    changeUserNameBlueprint,
)
from routes.createPost import (
    createPostBlueprint,
)
from routes.dashboard import (
    dashboardBlueprint,
)
from routes.editPost import (
    editPostBlueprint,
)
from routes.index import (
    indexBlueprint,
)
from routes.login import (
    loginBlueprint,
)
from routes.logout import (
    logoutBlueprint,
)
from routes.passwordReset import (
    passwordResetBlueprint,
)
from routes.post import postBlueprint
from routes.postsAnalytics import (
    analyticsBlueprint,
)
from routes.privacyPolicy import (
    privacyPolicyBlueprint,
)
from routes.returnPostAnalyticsData import (
    returnPostAnalyticsDataBlueprint,
)
from routes.returnPostBanner import (
    returnPostBannerBlueprint,
)
from routes.search import (
    searchBlueprint,
)
from routes.searchBar import (
    searchBarBlueprint,
)
from routes.setLanguage import (
    setLanguageBlueprint,
)
from routes.signup import (
    signUpBlueprint,
)
from routes.user import userBlueprint
from routes.verifyUser import (
    verifyUserBlueprint,
)
from settings import (
    APP_HOST,
    APP_NAME,
    APP_PORT,
    APP_ROOT_PATH,
    APP_SECRET_KEY,
    APP_VERSION,
    CUSTOM_LOGGER,
    DEBUG_MODE,
    DEFAULT_ADMIN,
    DEFAULT_ADMIN_EMAIL,
    DEFAULT_ADMIN_PASSWORD,
    DEFAULT_ADMIN_POINT,
    DEFAULT_ADMIN_PROFILE_PICTURE,
    DEFAULT_ADMIN_USERNAME,
    LOG_FILE_ROOT,
    LOG_FOLDER_ROOT,
    LOG_IN,
    RECAPTCHA,
    RECAPTCHA_BADGE,
    RECAPTCHA_COMMENT,
    RECAPTCHA_COMMENT_DELETE,
    RECAPTCHA_DELETE_USER,
    RECAPTCHA_LOGIN,
    RECAPTCHA_PASSWORD_CHANGE,
    RECAPTCHA_PASSWORD_RESET,
    RECAPTCHA_POST_CREATE,
    RECAPTCHA_POST_DELETE,
    RECAPTCHA_POST_EDIT,
    RECAPTCHA_PROFILE_PICTURE_CHANGE,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_SIGN_UP,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_USERNAME_CHANGE,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_VERIFY_USER,
    REGISTRATION,
    SESSION_PERMANENT,
    SMTP_MAIL,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_SERVER,
    STATIC_FOLDER,
    TEMPLATE_FOLDER,
    UI_NAME,
    WERKZEUG_LOGGER,
)
from utils.afterRequest import (
    afterRequestLogger,
)
from utils.beforeRequest.browserLanguage import browserLanguage
from utils.contextProcessor.isLogin import isLogin
from utils.contextProcessor.isRegistration import isRegistration
from utils.contextProcessor.recaptchaBadge import recaptchaBadge
from utils.contextProcessor.returnPostUrlID import returnPostUrlID
from utils.contextProcessor.returnPostUrlSlug import returnPostUrlSlug
from utils.contextProcessor.returnUserProfilePicture import returnUserProfilePicture
from utils.contextProcessor.translations import injectTranslations
from utils.dbChecker import (
    analyticsTable,
    commentsTable,
    dbFolder,
    postsTable,
    usersTable,
)
from utils.errorHandlers.csrfErrorHandler import (
    csrfErrorHandler,
)
from utils.errorHandlers.notFoundErrorHandler import (
    notFoundErrorHandler,
)
from utils.errorHandlers.unauthorizedErrorHandler import (
    unauthorizedErrorHandler,
)
from utils.log import Log
from utils.terminalASCII import terminalASCII
from utils.time import currentTimeStamp

startTime = currentTimeStamp()


print(terminalASCII())


Log.info("Starting...")


app = Flask(
    import_name=APP_NAME,
    root_path=APP_ROOT_PATH,
    static_folder=STATIC_FOLDER,
    template_folder=TEMPLATE_FOLDER,
)


app.jinja_options["autoescape"] = True


app.secret_key = APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = SESSION_PERMANENT


csrf = CSRFProtect(app)


app.context_processor(isLogin)
app.context_processor(recaptchaBadge)
app.context_processor(isRegistration)
app.context_processor(returnUserProfilePicture)
app.context_processor(returnPostUrlID)
app.context_processor(returnPostUrlSlug)
app.context_processor(injectTranslations)
app.before_request(browserLanguage)


match WERKZEUG_LOGGER:
    case True:
        Log.warning("Werkzeug default logger is enabled")

    case False:
        from logging import getLogger

        Log.info("Werkzeug default logger is disabled")

        getLogger("werkzeug").disabled = True


match CUSTOM_LOGGER:
    case True:
        Log.info("Custom logger is enabled")

    case False:
        Log.info("Custom logger is disabled")


Log.info(f"Debug mode: {DEBUG_MODE}")
Log.info(f"Name: {APP_NAME}")
Log.info(f"Version: {APP_VERSION}")
Log.info(f"Host: {APP_HOST}")
Log.info(f"Port: {APP_PORT}")
Log.info(f"Secret key: {APP_SECRET_KEY}")
Log.info(f"Session permanent: {SESSION_PERMANENT}")
Log.info(f"Root path: {APP_ROOT_PATH}")
Log.info(f"Log folder root: {LOG_FOLDER_ROOT}")
Log.info(f"Log file root: {LOG_FILE_ROOT}")
Log.info(f"Log in: {LOG_IN}")
Log.info(f"Registration: {REGISTRATION}")

Log.info(f"UI: {UI_NAME}")
Log.info(f"Template folder: {TEMPLATE_FOLDER}")
Log.info(f"Static folder: {STATIC_FOLDER}")

Log.info(f"SMTP server: {SMTP_SERVER}")
Log.info(f"SMTP port: {SMTP_PORT}")
Log.info(f"SMTP mail: {SMTP_MAIL}")
Log.info(f"SMTP password: {SMTP_PASSWORD}")


match RECAPTCHA:
    case True:
        match RECAPTCHA_SITE_KEY == "" or RECAPTCHA_SECRET_KEY == "":
            case True:
                Log.error(
                    "reCAPTCHA keys is unvalid this may cause the application to crash",
                )
                Log.error(
                    "Please check your recaptcha keys or set recaptcha to false from true in 'constants.py'",
                )
            case False:
                Log.info("reCAPTCHA is on")
                Log.info(f"reCAPTCHA recaptcha site key: {RECAPTCHA_SITE_KEY}")
                Log.info(f"reCAPTCHA secret key: {RECAPTCHA_SECRET_KEY}")
                Log.info(f"reCAPTCHA verify url: {RECAPTCHA_VERIFY_URL}")
                Log.info(f"reCAPTCHA badge: {RECAPTCHA_BADGE}")

                Log.info(f"reCAPTCHA login: {RECAPTCHA_LOGIN}")
                Log.info(f"reCAPTCHA sign up: {RECAPTCHA_SIGN_UP}")
                Log.info(f"reCAPTCHA post create: {RECAPTCHA_POST_CREATE}")
                Log.info(f"reCAPTCHA post edit: {RECAPTCHA_POST_EDIT}")
                Log.info(f"reCAPTCHA post delete: {RECAPTCHA_POST_DELETE}")
                Log.info(f"reCAPTCHA comment: {RECAPTCHA_COMMENT}")
                Log.info(f"reCAPTCHA comment delete: {RECAPTCHA_COMMENT_DELETE}")
                Log.info(f"reCAPTCHA password reset: {RECAPTCHA_PASSWORD_RESET}")
                Log.info(f"reCAPTCHA password change: {RECAPTCHA_PASSWORD_CHANGE}")
                Log.info(f"reCAPTCHA username change: {RECAPTCHA_USERNAME_CHANGE}")
                Log.info(f"reCAPTCHA verify user: {RECAPTCHA_VERIFY_USER}")
                Log.info(f"reCAPTCHA delete user: {RECAPTCHA_DELETE_USER}")
                Log.info(
                    f"reCAPTCHA user profile picture change: {RECAPTCHA_PROFILE_PICTURE_CHANGE}",
                )
                Log.info(
                    f"reCAPTCHA profile picture change: {RECAPTCHA_PROFILE_PICTURE_CHANGE}",
                )
    case False:
        Log.info("reCAPTCHA is off")


match DEFAULT_ADMIN:
    case True:
        Log.info("Default admin is on")
        Log.info(f"Default admin username: {DEFAULT_ADMIN_USERNAME}")
        Log.info(f"Default admin email: {DEFAULT_ADMIN_EMAIL}")
        Log.info(f"Default admin password: {DEFAULT_ADMIN_PASSWORD}")
        Log.info(f"Default admin point: {DEFAULT_ADMIN_POINT}")
        Log.info(f"Default admin profile picture: {DEFAULT_ADMIN_PROFILE_PICTURE}")
    case False:
        Log.info("Default admin is off")


dbFolder()
usersTable()
postsTable()
commentsTable()
analyticsTable()


@app.errorhandler(404)
def notFound(e):
    return notFoundErrorHandler(e)


@app.errorhandler(401)
def unauthorized(e):
    return unauthorizedErrorHandler(e)


@app.errorhandler(CSRFError)
def csrfError(e):
    return csrfErrorHandler(e)


@app.after_request
def afterRequest(response):
    return afterRequestLogger(response)


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
app.register_blueprint(setLanguageBlueprint)
app.register_blueprint(privacyPolicyBlueprint)
app.register_blueprint(passwordResetBlueprint)
app.register_blueprint(changeUserNameBlueprint)
app.register_blueprint(changePasswordBlueprint)
app.register_blueprint(changeLanguageBlueprint)
app.register_blueprint(adminPanelUsersBlueprint)
app.register_blueprint(adminPanelPostsBlueprint)
app.register_blueprint(accountSettingsBlueprint)
app.register_blueprint(returnPostBannerBlueprint)
app.register_blueprint(adminPanelCommentsBlueprint)
app.register_blueprint(changeProfilePictureBlueprint)
app.register_blueprint(analyticsBlueprint)
app.register_blueprint(returnPostAnalyticsDataBlueprint)


match __name__:
    case "__main__":
        Log.info(f"Running on http://{APP_HOST}:{APP_PORT}")

        Log.success("App started")

        print(terminalASCII())

        app.run(debug=DEBUG_MODE, host=APP_HOST, port=APP_PORT)

        endTime = currentTimeStamp()

        runTime = endTime - startTime

        runTime = str(timedelta(seconds=runTime))

        Log.info(f"Run time: {runTime} ")

        Log.info("Shut down")

        Log.warning("App shut down")

        print(terminalASCII())
