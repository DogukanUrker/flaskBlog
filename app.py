from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, PasswordField, StringField, validators


class registerForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25)],
        render_kw={"placeholder": "username"},
    )
    email = StringField(
        "Email", [validators.Length(min=6, max=50)], render_kw={"placeholder": "email"}
    )
    password = PasswordField(
        "Passowrd", [validators.Length(min=8)], render_kw={"placeholder": "password"}
    )


class loginForm(Form):
    userName = StringField(
        "Username",
        [validators.Length(min=4, max=25)],
        render_kw={"placeholder": "username"},
    )
    password = PasswordField(
        "Passowrd", [validators.Length(min=8)], render_kw={"placeholder": "password"}
    )


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db.init_app(app)


class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String)
    posts = db.Column(db.String)
    password = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template(
        "index.html",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = loginForm(request.form)
    if request.method == "POST":
        userName = request.form["userName"]
        password = request.form["password"]
        try:
            user = db.session.execute(
                db.select(User).filter_by(userName=userName)
            ).one()
        except:
            return "no user"

        return render_template("login.html", form=form, user=user)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = registerForm(request.form)
    if request.method == "POST":
        user = User(
            userName=request.form["userName"],
            email=request.form["email"],
            password=request.form["password"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    return render_template("signup.html", form=form)


@app.route("/createpost")
def createPost():
    return render_template(
        "createPost.html",
    )


@app.route("/<postID>")
def post(postID):
    return "post will be display here"


if __name__ == "__main__":
    app.run(debug=True)
