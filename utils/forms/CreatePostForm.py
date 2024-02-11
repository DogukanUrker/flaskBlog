"""
This file contains class that are used to create CreatePostForm for the application.
"""

# Importing necessary modules from WTForms library
from wtforms import (
    Form,  # Importing the base class for forms
    FileField,  # Importing the field class for file uploads
    validators,  # Importing validators for form fields
    SelectField,  # Importing the field class for dropdown/select inputs
    StringField,  # Importing the field class for string/text inputs
    TextAreaField,  # Importing the field class for multi-line text inputs
)

# Import default form style
from .FormInputStyle import inputStyle


# Form class for Creating Post
class CreatePostForm(Form):
    """
    This class creates a form for creating a post.
    """

    # StringField for post title with validators for length and input requirement
    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "post title"},
    )
    # StringField for post tags with input requirement validator
    postTags = StringField(
        "Post Tags",
        [validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "tags"},
    )
    # TextAreaField for post content with validator for minimum length
    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=50)],
    )
    # FileField for post banner with input requirement validator
    postBanner = FileField(
        "Post Banner",
        [validators.InputRequired()],
        render_kw={"placeholder": "post banner"},
    )
    # SelectField for post category with input requirement validator and choices
    postCategory = SelectField(
        "Post Category",
        [validators.InputRequired()],
        choices=[
            ("Other", "Other"),
            ("Apps", "Apps"),
            ("Art", "Art"),
            ("Books", "Books"),
            ("Business", "Business"),
            ("Code", "Code"),
            ("Education", "Education"),
            ("Finance", "Finance"),
            ("Foods", "Foods"),
            ("Games", "Games"),
            ("Health", "Health"),
            ("History", "History"),
            ("Movies", "Movies"),
            ("Music", "Music"),
            ("Nature", "Nature"),
            ("Science", "Science"),
            ("Series", "Series"),
            ("Sports", "Sports"),
            ("Technology", "Technology"),
            ("Travel", "Travel"),
            ("Web", "Web"),
        ],
        render_kw={"class": inputStyle() + " text-rose-500"},
    )
