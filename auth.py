from wtforms import Form, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length, Email

class Register(Form):
    username = StringField("Username", [Length(min=4, max=20), InputRequired()])
    email = StringField("Email", [InputRequired(), Email()])
    password = PasswordField("Password", [InputRequired()])
    confirm_password = PasswordField("Confirm Password", [InputRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

class Login(Form):
    email = StringField("Email", [Email(), InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    submit = SubmitField("Login")