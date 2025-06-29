"""
This file contains class that are used to create ChangeProfilePictureForm for the application.
"""

from wtforms import (
    Form,
    StringField,
    validators,
)

from .FormInputStyle import inputStyle


class ChangeProfilePictureForm(Form):
    """
    This class creates a form for changing the profile picture.
    """

    newProfilePictureSeed = StringField(
        "ProfilePictureSeed",
        [validators.InputRequired()],
        render_kw={
            "class": inputStyle(),
        },
    )
