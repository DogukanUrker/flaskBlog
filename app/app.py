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
    about_blueprint,
)
from routes.accountSettings import (
    account_settings_blueprint,
)
from routes.adminPanel import (
    admin_panel_blueprint,
)
from routes.adminPanelComments import (
    admin_panel_comments_blueprint,
)
from routes.adminPanelPosts import (
    admin_panel_posts_blueprint,
)
from routes.adminPanelUsers import (
    admin_panel_users_blueprint,
)
from routes.category import (
    category_blueprint,
)
from routes.changeLanguage import (
    change_language_blueprint,
)
from routes.changePassword import (
    change_password_blueprint,
)
from routes.changeProfilePicture import (
    change_profile_picture_blueprint,
)
from routes.changeUserName import (
    change_user_name_blueprint,
)
from routes.createPost import (
    create_post_blueprint,
)
from routes.dashboard import (
    dashboard_blueprint,
)
from routes.editPost import (
    edit_post_blueprint,
)
from routes.index import (
    index_blueprint,
)
from routes.login import (
    login_blueprint,
)
from routes.logout import (
    logout_blueprint,
)
from routes.passwordReset import (
    password_reset_blueprint,
)
from routes.post import post_blueprint
from routes.postsAnalytics import (
    analytics_blueprint,
)
from routes.privacyPolicy import (
    privacy_policy_blueprint,
)
from routes.returnPostAnalyticsData import (
    return_post_analytics_data_blueprint,
)
from routes.returnPostBanner import (
    return_post_banner_blueprint,
)
from routes.search import (
    search_blueprint,
)
from routes.searchBar import (
    search_bar_blueprint,
)
from routes.setLanguage import (
    set_language_blueprint,
)
from routes.setTheme import (
    set_theme_blueprint,
)
from routes.signup import (
    sign_up_blueprint,
)
from routes.user import user_blueprint
from routes.verifyUser import (
    verify_user_blueprint,
)
from settings import Settings
from utils.afterRequest import after_request_logger
from utils.beforeRequest.browserLanguage import browser_language
from utils.contextProcessor.isLogin import is_login
from utils.contextProcessor.isRegistration import is_registration
from utils.contextProcessor.markdown import markdown_processor
from utils.contextProcessor.returnPostUrlID import returnPostUrlID
from utils.contextProcessor.returnPostUrlSlug import returnPostUrlSlug
from utils.contextProcessor.returnUserProfilePicture import returnUserProfilePicture
from utils.contextProcessor.translations import inject_translations
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
from utils.generateUrlIdFromPost import get_slug_from_post_title
from utils.log import Log
from utils.terminalASCII import terminal_ascii
from utils.time import current_time_stamp

start_time = current_time_stamp()


print(terminal_ascii())


Log.info("Starting...")


app = Flask(
    import_name=Settings.APP_NAME,
    root_path=Settings.APP_ROOT_PATH,
)


app.jinja_options["autoescape"] = True


app.secret_key = Settings.APP_SECRET_KEY
app.config["SESSION_PERMANENT"] = Settings.SESSION_PERMANENT


csrf = CSRFProtect(app)


app.context_processor(is_login)

app.context_processor(is_registration)
app.context_processor(returnUserProfilePicture)
app.context_processor(returnPostUrlID)
app.context_processor(returnPostUrlSlug)
app.context_processor(inject_translations)
app.context_processor(markdown_processor)
app.before_request(browser_language)
app.jinja_env.globals.update(get_slug_from_post_title=get_slug_from_post_title)

if Settings.WERKZEUG_LOGGER:
    Log.warning("Werkzeug default logger is enabled")
else:
    from logging import getLogger

    Log.info("Werkzeug default logger is disabled")

    getLogger("werkzeug").disabled = True


if Settings.TAMGA_LOGGER:
    Log.info("Custom logger is enabled")
else:
    Log.info("Custom logger is disabled")


Log.info(f"Debug mode: {Settings.DEBUG_MODE}")
Log.info(f"Name: {Settings.APP_NAME}")
Log.info(f"Version: {Settings.APP_VERSION}")
Log.info(f"Host: {Settings.APP_HOST}")
Log.info(f"Port: {Settings.APP_PORT}")
Log.info(f"Session permanent: {Settings.SESSION_PERMANENT}")
Log.info(f"Root path: {Settings.APP_ROOT_PATH}")
Log.info(f"Log folder root: {Settings.LOG_FOLDER_ROOT}")
Log.info(f"Log file root: {Settings.LOG_FILE_ROOT}")
Log.info(f"Log in: {Settings.LOG_IN}")
Log.info(f"Registration: {Settings.REGISTRATION}")

Log.info(f"SMTP server: {Settings.SMTP_SERVER}")
Log.info(f"SMTP port: {Settings.SMTP_PORT}")
Log.info(f"SMTP mail: {Settings.SMTP_MAIL}")


if Settings.RECAPTCHA:
    if Settings.RECAPTCHA_SITE_KEY == "" or Settings.RECAPTCHA_SECRET_KEY == "":
        Log.error(
            "reCAPTCHA keys is unvalid this may cause the application to crash",
        )
        Log.error(
            "Please check your recaptcha keys or set recaptcha to false from true in 'settings.py'",
        )
    else:
        Log.info("reCAPTCHA is on for login and signup pages")
        Log.info(f"reCAPTCHA recaptcha site key: {Settings.RECAPTCHA_SITE_KEY}")
        Log.info(f"reCAPTCHA verify url: {Settings.RECAPTCHA_VERIFY_URL}")

else:
    Log.info("reCAPTCHA is off")


if Settings.DEFAULT_ADMIN:
    Log.info("Default admin is on")
    Log.info(f"Default admin username: {Settings.DEFAULT_ADMIN_USERNAME}")
    Log.info(f"Default admin email: {Settings.DEFAULT_ADMIN_EMAIL}")
    Log.info(f"Default admin point: {Settings.DEFAULT_ADMIN_POINT}")
    Log.info(f"Default admin profile picture: {Settings.DEFAULT_ADMIN_PROFILE_PICTURE}")
else:
    Log.info("Default admin is off")


dbFolder()
usersTable()
postsTable()
commentsTable()
analyticsTable()


@app.errorhandler(404)
def not_found(e):
    return notFoundErrorHandler(e)


@app.errorhandler(401)
def unauthorized(e):
    return unauthorizedErrorHandler(e)


@app.errorhandler(CSRFError)
def csrf_error(e):
    return csrfErrorHandler(e)


@app.after_request
def after_request(response):
    response = after_request_logger(response)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.tailwindcss.com; "
        "img-src 'self' data: https: blob:; "
        "font-src 'self' https://cdn.jsdelivr.net;"
    )
    return response


app.register_blueprint(post_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(sign_up_blueprint)
app.register_blueprint(logout_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(edit_post_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(search_bar_blueprint)
app.register_blueprint(admin_panel_blueprint)
app.register_blueprint(create_post_blueprint)
app.register_blueprint(verify_user_blueprint)
app.register_blueprint(set_language_blueprint)
app.register_blueprint(set_theme_blueprint)
app.register_blueprint(privacy_policy_blueprint)
app.register_blueprint(password_reset_blueprint)
app.register_blueprint(change_user_name_blueprint)
app.register_blueprint(change_password_blueprint)
app.register_blueprint(change_language_blueprint)
app.register_blueprint(admin_panel_users_blueprint)
app.register_blueprint(admin_panel_posts_blueprint)
app.register_blueprint(account_settings_blueprint)
app.register_blueprint(return_post_banner_blueprint)
app.register_blueprint(admin_panel_comments_blueprint)
app.register_blueprint(change_profile_picture_blueprint)
app.register_blueprint(analytics_blueprint)
app.register_blueprint(return_post_analytics_data_blueprint)


if __name__ == "__main__":
    Log.info(f"Running on http://{Settings.APP_HOST}:{Settings.APP_PORT}")
    Log.success("App started")

    print(terminal_ascii())
    app.run(debug=Settings.DEBUG_MODE, host=Settings.APP_HOST, port=Settings.APP_PORT)

    end_time = current_time_stamp()
    run_time = end_time - start_time
    run_time = str(timedelta(seconds=run_time))

    Log.info(f"Run time: {run_time} ")
    Log.info("Shut down")
    Log.warning("App shut down")

    print(terminal_ascii())
