from . import app, bcrypt
from . import db
import secrets
from PIL import Image
from .forms import Register, Login, UpdateProfile, CreatePost
from flask import render_template, url_for, flash, redirect, request
from .models import User, Post
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import os

@app.route("/")
def home():
    posts = Post.query.all()
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

@app.route("/profile/", methods=["GET", "POST"])
@login_required
def profile():
    form = UpdateProfile()
    if request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.picture.data = current_user.image
    else:
        if form.validate_on_submit():
            if form.picture.data:
                current_user.image = save_pic(form.picture.data)
            current_user.username = form.username.data
            current_user.email = form.email.data
            
            db.session.commit()
            flash("Your profile has been updated successfully", "success")
            return (redirect(url_for("profile")))
    image = url_for("static", filename=current_user.image)
    return (render_template("profile.html", title="Profile", image=image, form=form))


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = CreatePost()
    if form.validate_on_submit():
        post = Post(
                title=form.title.data,
                content=form.text.data,
                user_id=current_user.id,
                date=datetime.now()
                )
        db.session.add(post)
        db.session.commit()
        flash("Post creted", "success")
        return redirect(url_for("home"))
    
    return (render_template("thoughts.html", title="Thoughts", form=form))


# Get indiviual post
@app.route("/post/<int:_id>")
def get_post(_id):
    post = Post.query.get_or_404(_id)
    form = CreatePost()
    
    return render_template("thought.html", post=post, title="Thought", form=form)




# Helper functions
def save_pic(picture):
    base = secrets.token_hex(8)
    _, ext = os.path.splitext(picture.filename)
    base = base + ext
    path = os.path.join(app.root_path, "static", base)

    img = Image.open(picture)
    img.thumbnail((150, 150))
    img.save(path)
    
    return base

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
