from helpers import secrets, socket

APP_HOST = socket.gethostbyname(socket.gethostname())
DEBUG_MODE = True
TAILWIND_UI = False
REGISTRATION = True
LOG_FILE_ROOT = "log.log"
APP_SECRET_KEY = secrets.token_urlsafe(32)
SESSION_PERMANENT = True
