"""
This file contains class that are used to create ChangePasswordForm for the application.
"""

from wtforms import (
    Form,
    PasswordField,
    validators,
)

from .FormInputStyle import inputStyle


class ChangePasswordForm(Form):
    """
    This class creates a form for changing the password.
    """

    oldPassword = PasswordField(
        "oldPassword",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle()},
    )

    password = PasswordField(
        "password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle()},
    )

    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle()},
    )
