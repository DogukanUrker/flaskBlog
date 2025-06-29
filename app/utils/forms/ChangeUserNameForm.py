"""
This file contains class that are used to create ChangeUserNameForm for the application.
"""

from wtforms import (
    Form,
    StringField,
    validators,
)

from .FormInputStyle import inputStyle


class ChangeUserNameForm(Form):
    """
    This class creates a form for changing the username.
    """

    newUserName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle()},
    )
