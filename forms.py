"""
This file contains classes that are used to create forms for the application.
"""

from wtforms import (
    Form,
    FileField,
    validators,
    EmailField,
    SelectField,
    StringField,
    PasswordField,
    TextAreaField,
)


def inputStyle():
    """
    This function creates a style for the input fields.
    """
    return "w-72 h-12 mb-4 mx-auto p-2 rounded-md text-center outline-rose-500 bg-transparent focus:outline-none focus:ring focus:ring-rose-500 duration-100 border-2 border-gray-500/25 focus:border-0 block shadow-md select-none"


class CommentForm(Form):
    """
    This class creates a form for commenting.
    """

    comment = TextAreaField(
        "Comment",
        [validators.Length(min=20, max=500), validators.InputRequired()],
        render_kw={"placeholder": "What are your thoughts?"},
    )


class LoginForm(Form):
    """
    This class creates a form for logging in.
    """

    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=5), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )


class CreatePostForm(Form):
    """
    This class creates a form for creating a post.
    """

    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "post title"},
    )
    postTags = StringField(
        "Post Tags",
        [validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "tags"},
    )
    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=50)],
    )
    postBanner = FileField(
        "Post Banner",
        [validators.InputRequired()],
        render_kw={"placeholder": "post banner"},
    )
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


class PasswordResetForm(Form):
    """
    This class creates a form for resetting the password.
    """

    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "email"},
    )
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "code"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )


class VerifyUserForm(Form):
    """
    This class creates a form for verifying the user.
    """

    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "code"},
    )


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
        render_kw={"class": inputStyle(), "placeholder": "old password"},
    )
    password = PasswordField(
        "password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "new password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )


class ChangeUserNameForm(Form):
    """
    This class creates a form for changing the username.
    """

    newUserName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "new username"},
    )


class ChangeProfilePictureForm(Form):
    """
    This class creates a form for changing the profile picture.
    """

    newProfilePictureSeed = StringField(
        "ProfilePictureSeed",
        [validators.InputRequired()],
        render_kw={
            "class": inputStyle(),
            "placeholder": "Enter seed for profile picture",
        },
    )


class SignUpForm(Form):
    """
    This class creates a form for signing up.
    """

    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "email"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )
