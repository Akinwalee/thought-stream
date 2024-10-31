from . import app, bcrypt
from . import db
from .auth import Register, Login
from flask import render_template, url_for, flash, redirect, request
from .models import User, Post
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
posts = [
    {
        "author": "Obatula Fuad",
        "title": "First Blog Post",
        "text": "This is the first post in this blog and I'm using it to test the flask Jinja templating thing",
        "date": datetime.now()
    },
    {
        "author": "Jognn Does",
        "title": "Second Blog Post",
        "text": "John Doe is John Doe because John Does loves John Does",
        "date": datetime.now()
    }
]


@app.route("/")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
    form = Register()
    if request.method == "POST":
        if form.validate_on_submit():
            create_user(form)
            flash(f"Welcome {form.username.data}! You can now login", "success")
            return (redirect(url_for("login")))
        else:
            flash(f"Email or Username already taken!", "danger")
            return (redirect(url_for("register")))
    return (render_template("register.html", title="Register", form=form))

@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return (redirect(url_for("home")))
    form = Login()
    if request.method == "POST" and form.validate_on_submit():
        user = get_user(form)
        if user:
            login_user(user, remember=form.remember.data)
            flash(f"Welcome {form.email.data}", "success")
            return (redirect(url_for("home")))
    return (render_template("login.html", title="Login", form=form))

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/profile/")
@login_required
def profile():
    return (render_template("profile.html", title="Profile"))



def create_user(form):
    password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    user = User(username=form.username.data,
                email=form.email.data,
                password=password)
    db.session.add(user)
    db.session.commit()

def get_user(form):
    user = User.query.filter_by(email=form.email.data).first()
    if not user:
        flash(f"The Email does not exist", "danger")
        return (False)
    pw_hash = user.password
    password = bcrypt.check_password_hash(pw_hash, form.password.data)
    if not password:
        flash(f"You entered an incorrect password", "danger")
        return (False)
    
    return (user)
    