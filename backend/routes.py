from . import app, bcrypt
from . import db
from .auth import Register, Login
from flask import render_template, url_for, flash, redirect, request
from .models import User, Post
from datetime import datetime

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
    form = Register()
    if request.method == "POST":
        if form.validate_on_submit():
            create_user(form)
            flash(f"YWelcome {form.username.data}! You can now login", "success")
            return (redirect(url_for("login")))
        else:
            flash(f"Account creation error!", "danger")
            print(form.errors.items())
            return (redirect(url_for("register")))
    return (render_template("register.html", title="Register", form=form))

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = Login()
    if request.method == "POST" and form.validate_on_submit():
        if form.email.data == "hello@gmail.com" and form.password.data == "12345":
            flash(f"Welcome {form.email.data}", "success")
            return (redirect(url_for("home")))
    return (render_template("login.html", title="Login", form=form))



def create_user(form):
    password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
    user = User(username=form.username.data,
                email=form.email.data,
                password=password)
    db.session.add(user)
    db.session.commit()