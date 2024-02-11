"""
This file contains class that are used to create PasswordResetForm for the application.
"""

# Importing necessary modules from WTForms library
from wtforms import (
    Form,  # Importing the base class for forms
    validators,  # Importing validators for form fields
    EmailField,  # Importing the field class for email inputs
    StringField,  # Importing the field class for string/text inputs
    PasswordField,  # Importing the field class for password inputs
)


# Import default form style
from .FormInputStyle import inputStyle


# Form class for Password Reset
class PasswordResetForm(Form):
    """
    This class creates a form for resetting the password.
    """

    # StringField for username with validators for length and input requirement
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    # EmailField for email with validators for length and input requirement
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "email"},
    )
    # StringField for code with validators for length and input requirement
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "code"},
    )
    # PasswordField for password with validators for length and input requirement
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )
    # PasswordField for confirming password with validators for length and input requirement
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )
