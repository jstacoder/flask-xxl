from flask.ext.codemirror.fields import CodeMirrorField
from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from flask.ext.wtf.recaptcha.fields import RecaptchaField
from wtforms import fields,validators
from settings import get_choices
from page.fields import CKTextEditorField

class EditContentForm(Form):
    content = CKTextEditorField('content')


class ContactUsForm(Form):
    name = fields.StringField('Name',validators=[validators.InputRequired()])
    email = fields.StringField('Email',validators=[validators.InputRequired()])
    subject = fields.SelectField('Subject',validators=[validators.Optional()],choices=get_choices())
    message = fields.TextAreaField('Message',validators=[validators.InputRequired()])
    recaptcha = RecaptchaField('are you a human')
    ip_address = fields.HiddenField()



class FrontendEditPageForm(Form):
    title = fields.StringField('Title')
    content = PageDownField('Content')
