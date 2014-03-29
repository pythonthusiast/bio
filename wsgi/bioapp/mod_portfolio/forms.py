from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email


class PortoForm(Form):
    portfolio_id = HiddenField()
    title = TextField('Title', validators=[
            validators.Length(min=3, message=(u'Title must be longer, at least 3 characters'))
            ])
    description = TextField('Description', validators=[
            validators.Length(min=10, message=(u'Please give a longer description, at least 10 characters'))
            ])
    tags = TextField('Tags', validators=[
            validators.Length(min=2, message=(u'The tag at least having 2 characters length'))
            ])