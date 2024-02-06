"""
This file contains classes that are used to create forms for the application.
"""

# Importing necessary modules from WTForms library
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


# Function to define the style for input fields
def inputStyle():
    """
    This function creates a style for the input fields.
    """
    return "w-72 h-12 mb-4 mx-auto p-2 rounded-md text-center outline-rose-500 bg-transparent focus:outline-none focus:ring focus:ring-rose-500 duration-100 border-2 border-gray-500/25 focus:border-0 block shadow-md select-none"


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


# Form class for Login
class LoginForm(Form):
    """
    This class creates a form for logging in.
    """

    # StringField for username with validators for length and input requirement
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    # PasswordField for password with validators for length and input requirement
    password = PasswordField(
        "Password",
        [validators.Length(min=5), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )


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


# Form class for Password Reset
class PasswordResetForm(Form):
    """
    This class creates a form for resetting the password.
    """

    # StringField for username with validators for length and input requirement
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    # EmailField for email with validators for length and input requirement
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "email"},
    )
    # StringField for code with validators for length and input requirement
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "code"},
    )
    # PasswordField for password with validators for length and input requirement
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )
    # PasswordField for confirming password with validators for length and input requirement
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )


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


# Form class for Changing Password
class ChangePasswordForm(Form):
    """
    This class creates a form for changing the password.
    """

    # PasswordField for old password with validators for length and input requirement
    oldPassword = PasswordField(
        "oldPassword",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "old password"},
    )
    # PasswordField for new password with validators for length and input requirement
    password = PasswordField(
        "password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "new password"},
    )
    # PasswordField for confirming new password with validators for length and input requirement
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )


# Form class for Changing Username
class ChangeUserNameForm(Form):
    """
    This class creates a form for changing the username.
    """

    # StringField for new username with validators for length and input requirement
    newUserName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "new username"},
    )


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
            "placeholder": "Enter seed for profile picture",
        },
    )


# Form class for Signing Up
class SignUpForm(Form):
    """
    This class creates a form for signing up.
    """

    # StringField for username with validators for length and input requirement
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "username"},
    )
    # EmailField for email with validators for length and input requirement
    email = EmailField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"class": inputStyle(), "placeholder": "email"},
    )
    # PasswordField for password with validators for length and input requirement
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "password"},
    )
    # PasswordField for confirming password with validators for length and input requirement
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle(), "placeholder": "confirm your password"},
    )
