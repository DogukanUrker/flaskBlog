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

# Importing constants and forms from other modules

from constants import (  # Constants related to SMTP settings
    SMTP_MAIL,
    SMTP_PORT,
    SMTP_SERVER,
    SMTP_PASSWORD,
)

from constants import (  # Importing multiple constants related to the application configuration
    LOG_IN,
    APP_NAME,
    APP_VERSION,
    BREAKER_TEXT,
    REGISTRATION,
    LOG_FILE_ROOT,
    DB_USERS_ROOT,
    DB_POSTS_ROOT,
    BREAKER_TEXT,
    DB_COMMENTS_ROOT,
)

from constants import (  # Importing constants related to reCAPTCHA configuration
    RECAPTCHA,
    RECAPTCHA_BADGE,
    RECAPTCHA_LOGIN,
    RECAPTCHA_COMMENT,
    RECAPTCHA_SIGN_UP,
    RECAPTCHA_SITE_KEY,
    RECAPTCHA_POST_EDIT,
    RECAPTCHA_SECRET_KEY,
    RECAPTCHA_VERIFY_URL,
    RECAPTCHA_VERIFY_USER,
    RECAPTCHA_POST_CREATE,
    RECAPTCHA_DELETE_USER,
    RECAPTCHA_POST_DELETE,
    RECAPTCHA_COMMENT_DELETE,
    RECAPTCHA_PASSWORD_RESET,
    RECAPTCHA_PASSWORD_CHANGE,
    RECAPTCHA_USERNAME_CHANGE,
    RECAPTCHA_PROFILE_PICTURE_CHANGE,
)
from email.message import EmailMessage  # Email handling

from passlib.hash import sha512_crypt as encryption  # Password hashing library

from forms import (  # Importing various form classes used in the application
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


# Function to get the current system time zone
def currentTimeZone():
    """
    Returns the current system time zone as a string.
    """
    return tzname[0]


# Function to get the current date in the format "dd.mm.yy"
def currentDate():
    """
    Returns the current date as a string in the format "dd.mm.yy".
    """
    return datetime.now().strftime("%d.%m.%y")


# Function to get the current time
def currentTime(seconds=False, microSeconds=False):
    """
    Returns the current time as a string in the format "HH:MM" or "HH:MM:SS" depending on the value of the seconds parameter. If the microSeconds parameter is set to True, the time will include microseconds as well.
    """
    match seconds:
        case False:
            return datetime.now().strftime("%H:%M")
        case True:
            match microSeconds:
                case True:
                    return datetime.now().strftime("%H:%M:%S.%f")
                case False:
                    return datetime.now().strftime("%H:%M:%S")


# Function to get the current timestamp
def currentTimeStamp():
    """
    Returns the current time stamp as an integer.
    """
    timeStamp = datetime.now().timestamp()  # Get current timestamp
    timeStamp = int(timeStamp)  # Convert to integer
    return timeStamp


# Function to print messages with color and log them
def message(
    color="0",
    message="NO MESSAGE CONTENT",
    breaker=False,
):
    """
    Prints a colored message to the console and appends it to the log file. The color parameter can be any number between 0 and 9, where 0 is the default color and 9 is the brightest color. The breaker parameter can be set to True to print a line breaker before the message.
    """
    match breaker:
        case True:
            # Print line breaker with specified color code
            print(f"\033[9{color}m {BREAKER_TEXT}\033[0m")
            # Append line breaker to log file
            logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
            logFile.write(BREAKER_TEXT + "\n")
            logFile.close()
        case False:
            # Print message with timestamp and color code
            print(
                f"\n\033[94m[{currentDate()}\033[0m"
                f"\033[95m {currentTime(seconds=True)}\033[0m"
                f"\033[94m {currentTimeZone()}] \033[0m"
                f"\033[9{color}m {message}\033[0m\n"
            )
            # Append message to log file with timestamp
            logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
            logFile.write(
                f"[{currentDate()}"
                f"|{currentTime(seconds=True,microSeconds=True)}"
                f"|{currentTimeZone()}]"
                "\t"
                f"{message}\n"
            )
            logFile.close()


# Function to add points to a user
def addPoints(points, user):
    """
    Adds the specified number of points to the user with the specified username.
    """
    connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the SQLite database
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(  # Execute SQL query to update user points
        """update users set points = points+? where userName = ? """,
        [(points), (user)],
    )
    connection.commit()  # Commit changes to the database
    message("2", f'{points} POINTS ADDED TO "{user}"')


# Function to get the profile picture of a user
def getProfilePicture(userName):
    """
    Returns the profile picture of the user with the specified username.
    """
    connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the SQLite database
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(  # Execute SQL query to retrieve user profile picture
        """select profilePicture from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    return cursor.fetchone()[0]  # Fetch the profile picture value


# Function to change the role of a user
def changeUserRole(userName):
    """
    Changes the role of the user with the specified username.
    """
    userName = userName.lower()  # Convert username to lowercase
    connection = sqlite3.connect(DB_USERS_ROOT)  # Connect to the SQLite database
    cursor = connection.cursor()  # Create a cursor object
    cursor.execute(  # Execute SQL query to retrieve user role
        """select role from users where lower(userName) = ? """,
        [(userName)],
    )
    role = cursor.fetchone()[0]  # Fetch the role value
    match role:
        case "admin":
            newRole = "user"
        case "user":
            newRole = "admin"
    cursor.execute(  # Execute SQL query to update user role
        """update users set role = ? where lower(userName) = ? """,
        [(newRole), (userName)],
    )
    message(  # Log the role change event
        "2",
        f'ADMIN: "{session["userName"]}" CHANGED USER: "{userName}"s ROLE TO "{newRole}" ',
    )
    connection.commit()  # Commit changes to the database
    match session["userName"].lower() == userName:
        case True:
            return redirect("/")


# Function to return the terminal ASCII art
def terminalASCII():
    """
    This function returns a string containing the terminal ASCII art.
    """
    return """\033[91m
  __ _           _    ____  _                   ____  
 / _| | __ _ ___| | _| __ )| | ___   __ ___   _|___ \ 
| |_| |/ _` / __| |/ /  _ \| |/ _ \ / _` \ \ / / __) |
|  _| | (_| \__ \   <| |_) | | (_) | (_| |\ V / / __/ 
|_| |_|\__,_|___/_|\_\____/|_|\___/ \__, | \_/ |_____|
                                    |___/             
                                      by Dogukan Urker
    \033[0m"""
