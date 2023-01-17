from wtforms import Form, PasswordField, StringField, TextAreaField, validators


class commentForm(Form):
    comment = StringField(
        "Comment",
        [validators.Length(min=20, max=500)],
        render_kw={"placeholder": "your comment min 20 max 500 keys"},
    )


class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    password = PasswordField(
        "Password",
        [validators.Length(min=8), validators.InputRequired()],
        render_kw={"placeholder": "password"},
    )


class createPostForm(Form):
    postTitle = StringField(
        "Post Title",
        [validators.Length(min=4, max=75), validators.InputRequired()],
        render_kw={"placeholder": "post title"},
    )
    postTags = StringField(
        "Post Tags", [validators.InputRequired()], render_kw={"placeholder": "tags"}
    )
    postContent = TextAreaField(
        "Post Content",
        [validators.Length(min=50), validators.InputRequired()],
    )


class signUpForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25), validators.InputRequired()],
        render_kw={"placeholder": "username"},
    )
    email = StringField(
        "Email",
        [validators.Length(min=6, max=50), validators.InputRequired()],
        render_kw={"placeholder": "email"},
    )
    password = PasswordField(
        "Password",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "password"},
    )
    passwordConfirm = PasswordField(
        "passwordConfirm",
        [
            validators.Length(min=8),
            validators.InputRequired(),
        ],
        render_kw={"placeholder": "confirm your password"},
    )
