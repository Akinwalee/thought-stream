from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, Email, ValidationError
from flask_wtf import FlaskForm
from .models import User

class Register(FlaskForm):
    username = StringField("Username", [Length(min=4, max=20), InputRequired()])
    email = StringField("Email", [InputRequired(), Email()])
    password = PasswordField("Password", [InputRequired()])
    confirm_password = PasswordField("Confirm Password", [InputRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data)
        if user:
            raise ValidationError("A user with this username already exist")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data)
        if user:
            raise ValidationError("A user with this email already exist")

class Login(FlaskForm):
    email = StringField("Email", [Email(), InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField("Login")