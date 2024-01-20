from wtforms import validators, Form, StringField, PasswordField, TextAreaField

inputStyle = "w-72 h-12 mb-4 mx-auto p-2 rounded-md text-center outline-rose-500 bg-transparent focus:outline-none focus:ring focus:ring-rose-500 duration-100 border-2 border-gray-500/25 focus:border-0 block shadow-md select-none"


class commentForm(Form):
    comment = TextAreaField(
        "Comment",
        [validators.Length(min=20, max=500), validators.InputRequired()],
        render_kw={"placeholder": "leave a comment"},
    )


class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "username"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=5), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "password"},
    )


class createPostForm(Form):
    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "post title"},
    )
    postTags = StringField(
        "Post Tags",
        [validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "tags"},
    )
    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=50)],
    )


class passwordResetForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "username"},
    )
    email = StringField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "email"},
    )
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "code"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle, "placeholder": "password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle, "placeholder": "confirm your password"},
    )


class verifyUserForm(Form):
    code = StringField(
        "code",
        [validators.Length(min=4, max=4), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "code"},
    )


class changePasswordForm(Form):
    oldPassword = PasswordField(
        "oldPassword",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle, "placeholder": "old password"},
    )
    password = PasswordField(
        "password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle, "placeholder": "new password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle, "placeholder": "confirm your password"},
    )


class changeUserNameForm(Form):
    newUserName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "new username"},
    )


class changeProfilePictureForm(Form):
    newProfilePictureSeed = StringField(
        "ProfilePictureSeed",
        [validators.InputRequired()],
        render_kw={
            "class": inputStyle,
            "placeholder": "Enter seed for profile picture",
        },
    )


class signUpForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "username"},
    )
    email = StringField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"class": inputStyle, "placeholder": "email"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle, "placeholder": "password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"class": inputStyle, "placeholder": "confirm your password"},
    )
