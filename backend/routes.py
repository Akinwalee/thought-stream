from . import app
from .auth import Register, Login
from flask import render_template, url_for, flash, redirect, request
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
            flash(f"Account created for user {form.username.data}!", "success")
            return (redirect(url_for("home")))
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
