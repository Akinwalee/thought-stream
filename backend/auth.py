from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, Email, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from .models import User
from flask_login import current_user

class Register(FlaskForm):
    username = StringField("Username", [Length(min=4, max=20), InputRequired()])
    email = StringField("Email", [InputRequired(), Email()])
    password = PasswordField("Password", [InputRequired()])
    confirm_password = PasswordField("Confirm Password", [InputRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("A user with this username already exist")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("A user with this email already exist")

class Login(FlaskForm):
    email = StringField("Email", [Email(), InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField("Login")

class UpdateProfile(FlaskForm):
    email = StringField("Email", [Email()])
    username = StringField("Username", [Length(min=4, max=20)])
    picture = FileField("Profile Pic", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and username.data != current_user.username:
            raise ValidationError("A user with this username already exist")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and email.data != current_user.email:
            raise ValidationError("A user with this email already exist")