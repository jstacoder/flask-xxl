from flask.ext.codemirror.fields import CodeMirrorField
from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha.fields import RecaptchaField
from wtforms import fields,validators

from .fields import CKTextEditorField

class EditContentForm(Form):
    content = CKTextEditorField('content')


class ContactUsForm(Form):
    name = fields.StringField('Name',validators=[validators.InputRequired()])
    email = fields.StringField('Email',validators=[validators.InputRequired()])
    #subject = fields.SelectField('Subject',validators=[validators.Optional()],choices=get_choices())
    message = fields.TextAreaField('Message',validators=[validators.InputRequired()])
    recaptcha = RecaptchaField('are you a human')
    ip_address = fields.HiddenField()


class ContactUsSettingsForm(Form):
    address = fields.StringField('Business Address')
    email = fields.StringField('Contact Email')
    phone = fields.StringField('Contact Phone Number')
    hours = fields.StringField('Company Hours')
    facebook_link = fields.StringField('Facebook link')
    twitter_link = fields.StringField('twitter Link')
    google_link = fields.StringField('Google+ link')


class TestForm(Form):
    test = fields.RadioField(
            'test',
                choices = (
                    ('val','label'),
                    ('val2','label2'),
                    ('val3','label3'),
                    ('val4','label4'),
                )
    )

class AddPageForm(Form):
    pass

class FrontendEditPageForm(Form):
    title = fields.StringField('Title')
    content = PageDownField('Content')
