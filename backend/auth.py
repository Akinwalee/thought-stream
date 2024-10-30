from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, Email
from flask_wtf import FlaskForm


class Register(FlaskForm):
    username = StringField("Username", [Length(min=4, max=20), InputRequired()])
    email = StringField("Email", [InputRequired(), Email()])
    password = PasswordField("Password", [InputRequired()])
    confirm_password = PasswordField("Confirm Password", [InputRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

class Login(FlaskForm):
    email = StringField("Email", [Email(), InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField("Login")