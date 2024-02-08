from flaskwebgui import FlaskUI
from app import app

FlaskUI(app=app, server="flask").run()
