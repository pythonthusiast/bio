from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

class SignupForm(Form):
    email = TextField('Email address', validators=[
            Required('Please provide a valid email address'),
            Length(min=6, message=(u'Email address too short')),
            Email(message=(u'That\'s not a valid email address.'))
            ])
    password = PasswordField('Pick a secure password', validators=[
            Required(),
            Length(min=6, message=(u'Please give a longer password'))
            ])
    username = TextField('Choose your username', validators=[Required()])
    agree = BooleanField('I agree all your <a href="/static/tos.html">Terms of Services</a>', validators=[Required(u'You must accept our Terms of Service')])

class SigninForm(Form):
    username = TextField('Username', validators=[
            Required(),
            validators.Length(min=3, message=(u'Your username must be a minimum of 3'))
            ])
    password = PasswordField('Password', validators=[
            Required(),
            validators.Length(min=6, message=(u'Please give a longer password'))
            ])
    remember_me = BooleanField('Remember me', default = False)