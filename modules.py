"""
This module contains all the necessary functions and classes to run the application.
"""

from tamga import Tamga  # Importing Tamga Logger

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
from json import load  # Importing load function from json module
import uuid  # UUID (Universally Unique Identifier) generation
from re import sub  # Importing sub function from re module
import requests  # Importing requests module for http requests
from user_agents import parse  # Importing parse function to parsing user agent string
import geoip2  # Importing geoip2.databse
from geoip2 import database  # Importing geoip2.databse

# Importing constants
from constants import *  # noqa: F403

from email.message import EmailMessage  # Email handling

from passlib.hash import sha512_crypt as encryption  # Password hashing library

# Importing forms
from utils.forms.LoginForm import LoginForm  # Form class for user login
from utils.forms.SignUpForm import SignUpForm  # Form class for user sign-up
from utils.forms.CommentForm import CommentForm  # Form class for commenting
from utils.forms.CreatePostForm import (
    CreatePostForm,
)  # Form class for creating a new post
from utils.forms.VerifyUserForm import (
    VerifyUserForm,
)  # Form class for verifying user information
from utils.forms.PasswordResetForm import (
    PasswordResetForm,
)  # Form class for resetting a user's password
from utils.forms.ChangePasswordForm import (
    ChangePasswordForm,
)  # Form class for changing a user's password
from utils.forms.ChangeUserNameForm import (
    ChangeUserNameForm,
)  # Form class for changing a user's username
from utils.forms.ChangeProfilePictureForm import (
    ChangeProfilePictureForm,
)  # Form class for changing a user's profile picture

from flask import (
    Flask,  # Flask web application framework
    flash,  # Provides feedback messages to users
    abort,  # Stops processing and returns an HTTP error response
    url_for,  # Generates URLs for Flask routes
    request,  # Provides access to incoming request data
    session,  # Stores user session information
    redirect,  # Redirects the client to a different URL
    Blueprint,  # Helps organize related routes in Flask applications
    send_file,  # Sends a file to the client
    render_template,  # Renders HTML templates
    send_from_directory,  # Sends a file from a directory to the client
    make_response,  # Sends a response to client
)

# Importing the 'flashMessage' function from the 'utils.flashMessage' module for displaying flash messages.
from utils.flashMessage import flashMessage  # Function for displaying flash messages

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

# Importing the 'getPostUrlIDFromPost' function from 'utils.getPostUrlIdFromPost' module for retrieving post urlID from postID
from utils.getPostUrlIdFromPost import getPostUrlIdFromPost

# Importing the urlID generator and postUrlSlug for posts
from utils.generateUrlIdFromPost import generateurlID,  getSlugFromPostTitle

# Importing the 'terminalASCII' function from the 'utils.terminalASCII' module for displaying ASCII art in the terminal.
from utils.terminalASCII import terminalASCII

# Importing the 'isLogin' context processor from the 'utils.contextProcessor.isLogin' module
from utils.contextProcessor.isLogin import isLogin

# Importing the 'isRegistration' context processor from the 'utils.contextProcessor.isRegistration' module
from utils.contextProcessor.isRegistration import isRegistration

# Importing the 'recaptchaBadge' context processor from the 'utils.contextProcessor.recaptchaBadge' module
from utils.contextProcessor.recaptchaBadge import recaptchaBadge

# Importing the 'injectTranslations' function from the 'utils.contextProcessor.translations' module
from utils.contextProcessor.translations import injectTranslations

# Importing the 'browserLanguage' function from the 'utils.beforeRequest.browserLanguage' module
from utils.beforeRequest.browserLanguage import browserLanguage

# Importing the 'returnUserProfilePicture' context processor from the 'utils.contextProcessor.returnUserProfilePicture' module
from utils.contextProcessor.returnUserProfilePicture import returnUserProfilePicture

# importing the 'returnPostUrlID' context processor from the 'utils.contextProcessor.returnPostUrlID' module
from utils.contextProcessor.returnPostUrlID import returnPostUrlID

# importing the 'returnPostUrlSlug' context processor from the 'utils.contextProcessor.returnPostUrlSlug' module
from utils.contextProcessor.returnPostUrlSlug import returnPostUrlSlug

# Importing the 'Delete' class from the 'utils.delete' module for handling delete operations.
from utils.delete import Delete

# Importing the 'calculateReadTime' function from the 'utils.calculateReadTime' module for calculating reading time.
from utils.calculateReadTime import calculateReadTime

# Importing the getDataFromUserIP for analytics
from utils.getDataFromUserIP import getDataFromUserIP

# Importing the getAnalyticsPageCountryGraphData, getAnalyticsPageOSGraphData, getAnalyticsPageTrafficGraphData for analytics
from utils.getAnalyticsPageData import (
    getAnalyticsPageCountryGraphData,
    getAnalyticsPageOSGraphData,
    getAnalyticsPageTrafficGraphData,
)
