"""
This file contains class that are used to create ChangeUserNameForm for the application.
"""

# Importing necessary modules from WTForms library
from wtforms import (
    Form,  # Importing the base class for forms
    StringField,  # Importing the field class for string/text inputs
    validators,  # Importing validators for form fields
)

# Import default form style
from .FormInputStyle import inputStyle


# Form class for Changing Username
class ChangeUserNameForm(Form):
    """
    This class creates a form for changing the username.
    """

    # StringField for new username with validators for length and input requirement
    newUserName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle()},
    )
