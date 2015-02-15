from flask_wtf import Form
from wtforms import fields, validators

class BaseUserForm(Form):
    email = fields.StringField('Email Address',validators=[validators.InputRequired(),
                                validators.Email()])
    password = fields.PasswordField('Password',validators=[validators.DataRequired()])

class UserLoginForm(BaseUserForm):
    keep_me_logged_in = fields.BooleanField('Keep Me Logged In')


class UserSignupForm(BaseUserForm):
    confirm = fields.PasswordField('Confirm',validators=[validators.DataRequired(),
                                validators.EqualTo('password')])




