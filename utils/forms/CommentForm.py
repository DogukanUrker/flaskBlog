"""
This file contains class that are used to create CommentForm for the application.
"""

# Importing necessary modules from WTForms library
from wtforms import (
    Form,  # Importing the base class for forms
    validators,  # Importing validators for form fields
    TextAreaField,  # Importing the field class for multi-line text inputs
)


# Import default form style
from .FormInputStyle import inputStyle


# Form class for Comment
class CommentForm(Form):
    """
    This class creates a form for commenting.
    """

    # TextAreaField for comment with validators for length and input requirement
    comment = TextAreaField(
        "Comment",
        [validators.Length(min=20, max=500), validators.InputRequired()],
        render_kw={"placeholder": "What are your thoughts?"},
    )
