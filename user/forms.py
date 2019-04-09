from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, RadioField, FieldList, FormField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    fullname = StringField('Full Name', [validators.Required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')

class LoginForm(FlaskForm):
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=5, max=25)
        ])
    password = PasswordField('Password', [
            validators.Required(),
            validators.Length(min=5, max=80)
        ])


class PasswordBaseForm(FlaskForm):
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')


class ForgotForm(FlaskForm):
    email = EmailField('Email address',[
        validators.DataRequired(), 
        validators.Email()
        ])
    
class PasswordResetForm(PasswordBaseForm):
    current_password = PasswordField('Current Password',[
        validators.DataRequired(),
        validators.Length(min=4, max=80)
        ])
