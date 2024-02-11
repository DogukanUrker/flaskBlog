"""
This file contains class that are used to create VerifyUserForm for the application.
"""

# Importing necessary modules from WTForms library
from wtforms import (
    Form,  # Importing the base class for forms
    validators,  # Importing validators for form fields
    StringField,  # Importing the field class for string/text inputs
)


# Import default form style
from .FormInputStyle import inputStyle


# Form class for Verifying User
class VerifyUserForm(Form):
    """
    This class creates a form for verifying the user.
    """

    # StringField for code with validators for length and input requirement
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "code"},
    )
