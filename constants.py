"""
This module contains all the general application settings.
"""

# Import necessary modules from the modules module
from modules import secrets, socket


# Name of the Flask application
APP_NAME = "flaskBlog"  # (str)

# Version of the Flask application
APP_VERSION = "2.0.0-DEV"  # (str)

# Path to the root of the application files
APP_ROOT_PATH = "."  # (str)

# Hostname or IP address for the Flask application
APP_HOST = socket.gethostbyname(socket.gethostname())  # (str)

# Port number for the Flask application
APP_PORT = 5000  # (int)

# Toggle debug mode for the Flask application
DEBUG_MODE = True  # (bool)

# Name of the UI framework being used
UI_NAME = "tailwindUI"  # (str)

# Path to the templates folder
TEMPLATE_FOLDER = f"templates/{UI_NAME}"  # (str)

# Path to the static folder
STATIC_FOLDER = f"static/{UI_NAME}"  # (str)

# Toggle user login feature
LOG_IN = True  # (bool)

# Toggle user registration feature
REGISTRATION = True  # (bool)

### LOGGER SETTINGS ###
# Toggle custom logging feature
CUSTOM_LOGGER = True  # (bool)

# Toggle werkzeug logging feature
WERKZEUG_LOGGER = False  # (bool)

# Root path of the log folder
LOG_FOLDER_ROOT = "log/"  # (str)

# Root path of the log file
LOG_FILE_ROOT = LOG_FOLDER_ROOT + "log.log"  # (str)

# Root path of the danger log file
LOG_DANGER_FILE_ROOT = LOG_FOLDER_ROOT + "logDanger.log"  # (str)

# Root path of the success log file
LOG_SUCCESS_FILE_ROOT = LOG_FOLDER_ROOT + "logSuccess.log"  # (str)

# Root path of the warning log file
LOG_WARNING_FILE_ROOT = LOG_FOLDER_ROOT + "logWarning.log"  # (str)

# Root path of the info log file
LOG_INFO_FILE_ROOT = LOG_FOLDER_ROOT + "logInfo.log"  # (str)

# Root path of the app log file
LOG_APP_FILE_ROOT = LOG_FOLDER_ROOT + "logApp.log"  # (str)


# Secret key for Flask sessions
APP_SECRET_KEY = secrets.token_urlsafe(32)  # (str)

# Toggle permanent sessions for the Flask application
SESSION_PERMANENT = True  # (bool)

# Separator text used in log files
BREAKER_TEXT = "\n"  # (str)


### DATABASE SETTINGS ###

# Root path of the database folder
DB_FOLDER_ROOT = "db/"  # (str)

# Root path of the users database
DB_USERS_ROOT = DB_FOLDER_ROOT + "users.db"  # (str)

# Root path of the posts database
DB_POSTS_ROOT = DB_FOLDER_ROOT + "posts.db"  # (str)

# Root path of the comments database
DB_COMMENTS_ROOT = DB_FOLDER_ROOT + "comments.db"  # (str)


### SMTP MAIL SETTINGS ###

# SMTP server address
SMTP_SERVER = "smtp.gmail.com"  # (str)

# SMTP server port
SMTP_PORT = 587  # (int)

# SMTP mail address
SMTP_MAIL = "flaskblogdogukanurker@gmail.com"  # (str)

# SMTP mail password
SMTP_PASSWORD = "lsooxsmnsfnhnixy"  # (str)


### DEFAULT ADMIN ACCOUNT SETTINGS ###

# Toggle creation of default admin account
DEFAULT_ADMIN = True  # (bool)

# Default admin username
DEFAULT_ADMIN_USERNAME = "admin"  # (str)

# Default admin email address
DEFAULT_ADMIN_EMAIL = "admin@flaskblog.com"  # (str)

# Default admin password
DEFAULT_ADMIN_PASSWORD = "admin"  # (str)

# Default starting point score for admin
DEFAULT_ADMIN_POINT = 0  # (int)

# Default admin profile picture URL
DEFAULT_ADMIN_PROFILE_PICTURE = f"https://api.dicebear.com/7.x/identicon/svg?seed={DEFAULT_ADMIN_USERNAME}&radius=10"  # (str)


### RECAPTCHA SETTINGS ###

# Toggle reCAPTCHA verification
RECAPTCHA = False  # (bool)

# Toggle display of reCAPTCHA badge
RECAPTCHA_BADGE = False  # (bool)

# reCAPTCHA site key
RECAPTCHA_SITE_KEY = ""  # (str)

# reCAPTCHA secret key
RECAPTCHA_SECRET_KEY = ""  # (str)

# reCAPTCHA verify URL
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"  # (str)

# Toggle reCAPTCHA verification for different actions
RECAPTCHA_LOGIN = True  # (bool)
RECAPTCHA_SIGN_UP = True  # (bool)
RECAPTCHA_POST_CREATE = True  # (bool)
RECAPTCHA_POST_EDIT = True  # (bool)
RECAPTCHA_POST_DELETE = True  # (bool)
RECAPTCHA_COMMENT = True  # (bool)
RECAPTCHA_COMMENT_DELETE = True  # (bool)
RECAPTCHA_PASSWORD_RESET = True  # (bool)
RECAPTCHA_PASSWORD_CHANGE = True  # (bool)
RECAPTCHA_USERNAME_CHANGE = True  # (bool)
RECAPTCHA_VERIFY_USER = True  # (bool)
RECAPTCHA_DELETE_USER = True  # (bool)
RECAPTCHA_PROFILE_PICTURE_CHANGE = True  # (bool)
