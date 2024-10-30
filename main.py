from flask import Flask, render_template, url_for, flash, redirect, request
from datetime import datetime
from auth import Register, Login
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

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
    print(request.method)
    print(form.validate())
    if request.method == "POST":
        if form.validate():
            flash(f"Account created for user {form.username.data}!", "success")
            return (redirect(url_for("home")))
        else:
            flash(f"Account creation error!", "failure")
            print(form.errors.items())
            return (redirect(url_for("register")))
    return (render_template("register.html", title="Register", form=form))

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = Login()
    return (render_template("login.html", title="Login", form=form))

if __name__ == "__main__":
    app.run(debug=True)