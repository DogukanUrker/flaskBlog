"""
This file contains class that are used to create ChangePasswordForm for the application.
"""

# Importing necessary modules from WTForms library
from wtforms import (
    Form,  # Importing the base class for forms
    validators,  # Importing validators for form fields
    PasswordField,  # Importing the field class for password inputs
)

# Import default form style
from .FormInputStyle import inputStyle


# Form class for Changing Password
class ChangePasswordForm(Form):
    """
    This class creates a form for changing the password.
    """

    # PasswordField for old password with validators for length and input requirement
    oldPassword = PasswordField(
        "oldPassword",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "old password"},
    )
    # PasswordField for new password with validators for length and input requirement
    password = PasswordField(
        "password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "new password"},
    )
    # PasswordField for confirming new password with validators for length and input requirement
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )
