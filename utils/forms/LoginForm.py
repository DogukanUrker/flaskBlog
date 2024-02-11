"""
This file contains class that are used to create LoginForm for the application.
"""

from wtforms import (
    Form,  # Importing the base class for forms
    validators,  # Importing validators for form fields
    StringField,  # Importing the field class for string/text inputs
    PasswordField,  # Importing the field class for password inputs
)


# Import default form style
from .FormInputStyle import inputStyle


# Form class for Login
class LoginForm(Form):
    """
    This class creates a form for logging in.
    """

    # StringField for username with validators for length and input requirement
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    # PasswordField for password with validators for length and input requirement
    password = PasswordField(
        "Password",
        [validators.Length(min=5), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )
