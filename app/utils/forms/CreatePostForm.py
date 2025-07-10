"""
This file contains class that are used to create CreatePostForm for the application.
"""

from wtforms import (
    FileField,
    Form,
    SelectField,
    StringField,
    TextAreaField,
    validators,
)


class CreatePostForm(Form):
    """
    This class creates a form for creating a post.
    """

    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
    )

    postTags = StringField(
        "Post Tags",
        [validators.InputRequired()],
    )

    postAbstract = TextAreaField(
        "Post Abstract",
        [validators.Length(min=150, max=200), validators.InputRequired()],
    )

    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=50)],
    )

    postBanner = FileField("Post Banner")

    postCategory = SelectField(
        "Post Category",
        [validators.InputRequired()],
        choices=[
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
            ("Other", "Other"),
        ],
    )
