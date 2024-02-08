"""
This module contains all the necessary functions and classes to run the application.
"""

# Importing necessary modules and libraries
import os  # Operating system interfaces
import ssl  # Secure Sockets Layer (SSL) and Transport Layer Security (TLS) cryptographic protocols
import socket  # Socket module provides access to the BSD socket interface
import smtplib  # SMTP (Simple Mail Transfer Protocol) client session object
import secrets  # Generate secure random numbers for managing secrets
import sqlite3  # SQLite database library
from os import mkdir  # Importing mkdir function from os module directly
from io import BytesIO  # Importing BytesIO class from io module
from time import tzname  # Importing tzname attribute from time module
from random import randint  # Importing randint function from random module
from os.path import exists  # Importing exists function from os.path module
from datetime import datetime, timedelta  # Date and time handling
from requests import post as requestsPost  # HTTP library for sending POST requests

# Importing constants
from constants import *

from email.message import EmailMessage  # Email handling

from passlib.hash import sha512_crypt as encryption  # Password hashing library

from utils.forms import (  # Importing various form classes used in the application
    LoginForm,
    SignUpForm,
    CommentForm,
    CreatePostForm,
    VerifyUserForm,
    PasswordResetForm,
    ChangePasswordForm,
    ChangeUserNameForm,
    ChangeProfilePictureForm,
)

from flask import (  # Importing Flask components for web application development
    Flask,
    flash,
    abort,
    url_for,
    request,
    session,
    redirect,
    Blueprint,
    send_file,
    render_template,
    send_from_directory,
)


# Importing functions from the 'utils.time' module for handling date and time-related operations.
from utils.time import currentDate, currentTime, currentTimeStamp, currentTimeZone

# Importing the 'Log' class from the 'utils.log' module for logging messages.
from utils.log import Log

# Importing the 'addPoints' function from the 'utils.addPoints' module for adding points to user accounts.
from utils.addPoints import addPoints

# Importing the 'changeUserRole' function from the 'utils.changeUserRole' module for changing user roles.
from utils.changeUserRole import changeUserRole

# Importing the 'getProfilePicture' function from the 'utils.getProfilePicture' module for retrieving user profile pictures.
from utils.getProfilePicture import getProfilePicture

# Importing the 'terminalASCII' function from the 'utils.terminalASCII' module for displaying ASCII art in the terminal.
from utils.terminalASCII import terminalASCII


# Importing the 'isLogin' context processor from the 'utils.contextProcessor.isLogin' module
from utils.contextProcessor.isLogin import isLogin

# Importing the 'isRegistration' context processor from the 'utils.contextProcessor.isRegistration' module
from utils.contextProcessor.isRegistration import isRegistration

# Importing the 'recaptchaBadge' context processor from the 'utils.contextProcessor.recaptchaBadge' module
from utils.contextProcessor.recaptchaBadge import recaptchaBadge

# Importing the 'returnUserProfilePicture' context processor from the 'utils.contextProcessor.returnUserProfilePicture' module
from utils.contextProcessor.returnUserProfilePicture import returnUserProfilePicture

# Importing the 'Delete' class from the 'utils.delete' module for handling delete operations.
from utils.delete import Delete
