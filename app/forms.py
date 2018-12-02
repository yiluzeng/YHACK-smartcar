from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')

class RegForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    name = StringField('Full name', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    passconf = PasswordField('Confirm Password', validators=[validators.DataRequired(),validators.EqualTo('password',message='Passwords must match')])
    accept_tos = BooleanField('I accept the Terms of Service.',validators=[validators.DataRequired()])
    submit = SubmitField('Sign up')

class ChangePassForm(FlaskForm):
    passold = PasswordField('Old Password', validators=[validators.DataRequired()])
    passnew = PasswordField('New Password', validators=[validators.DataRequired()])
    passconf = PasswordField('Confirm Password', validators=[validators.DataRequired(),validators.EqualTo('passnew',message='Passwords must match')])
    submit = SubmitField('Change password')
