"""
This file contains class that are used to create ChangeProfilePictureForm for the application.
"""

# Importing necessary modules from WTForms library
from wtforms import (
    Form,  # Importing the base class for forms
    StringField,  # Importing the field class for string/text inputs
    validators,  # Importing validators for form fields
)

# Import default form style
from .FormInputStyle import inputStyle


# Form class for Changing Profile Picture
class ChangeProfilePictureForm(Form):
    """
    This class creates a form for changing the profile picture.
    """

    # StringField for new profile picture seed with input requirement validator
    newProfilePictureSeed = StringField(
        "ProfilePictureSeed",
        [validators.InputRequired()],
        render_kw={
            "class": inputStyle(),
        },
    )
