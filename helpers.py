"""
This module contains all the necessary functions and classes to run the application.
"""
import os
import ssl
import socket
import smtplib
import secrets
import sqlite3
from os import mkdir
from time import tzname
from random import randint
from os.path import exists
from datetime import datetime
from requests import post as requestsPost
from constants import (
    LOG_IN,
    APP_NAME,
    BREAKER_TEXT,
    REGISTRATION,
    LOG_FILE_ROOT,
    DB_USERS_ROOT,
    DB_POSTS_ROOT,
    BREAKER_TEXT,
    DB_COMMENTS_ROOT,
)
from constants import (
    RECAPTCHA,
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
from email.message import EmailMessage
from passlib.hash import sha256_crypt
from forms import (
    loginForm,
    signUpForm,
    commentForm,
    createPostForm,
    verifyUserForm,
    passwordResetForm,
    changePasswordForm,
    changeUserNameForm,
    changeProfilePictureForm,
)
from flask import (
    Flask,
    flash,
    abort,
    url_for,
    request,
    session,
    redirect,
    Blueprint,
    render_template,
    send_from_directory,
)


def currentTimeZone():
    """
    Returns the current system time zone as a string.
    """
    return tzname[0]


def currentDate():
    """
    Returns the current date as a string in the format "dd.mm.yy".
    """
    return datetime.now().strftime("%d.%m.%y")


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
            print(f"\033[9{color}m {BREAKER_TEXT}\033[0m")
            logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
            logFile.write(BREAKER_TEXT + "\n")
            logFile.close()
        case False:
            print(
                f"\n\033[94m[{currentDate()}\033[0m"
                f"\033[95m {currentTime(seconds=True)}\033[0m"
                f"\033[94m {currentTimeZone()}] \033[0m"
                f"\033[9{color}m {message}\033[0m\n"
            )
            logFile = open(LOG_FILE_ROOT, "a", encoding="utf-8")
            logFile.write(
                f"[{currentDate()}"
                f"|{currentTime(seconds=True,microSeconds=True)}"
                f"|{currentTimeZone()}]"
                "\t"
                f"{message}\n"
            )
            logFile.close()


def addPoints(points, user):
    """
    Adds the specified number of points to the user with the specified username.
    """
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """update users set points = points+? where userName = ? """,
        [(points), (user)],
    )
    connection.commit()
    message("2", f'{points} POINTS ADDED TO "{user}"')


def getProfilePicture(userName):
    """
    Returns the profile picture of the user with the specified username.
    """
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select profilePicture from users where lower(userName) = ? """,
        [(userName.lower())],
    )
    return cursor.fetchone()[0]


def changeUserRole(userName):
    """
    Changes the role of the user with the specified username.
    """
    userName = userName.lower()
    connection = sqlite3.connect(DB_USERS_ROOT)
    cursor = connection.cursor()
    cursor.execute(
        """select role from users where lower(userName) = ? """,
        [(userName)],
    )
    role = cursor.fetchone()[0]
    match role:
        case "admin":
            newRole = "user"
        case "user":
            newRole = "admin"
    cursor.execute(
        """update users set role = ? where lower(userName) = ? """,
        [(newRole), (userName)],
    )
    message(
        "2",
        f'ADMIN: "{session["userName"]}" CHANGED USER: "{userName}"s ROLE TO "{newRole}" ',
    )
    connection.commit()
    match session["userName"].lower() == userName:
        case True:
            return redirect("/")
