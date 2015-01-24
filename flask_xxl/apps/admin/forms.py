from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import QuerySelectField
from wtforms import fields, validators,widgets
from flask_pagedown.fields import PageDownField
from flask_codemirror.fields import CodeMirrorField
from ..page.fields import CKTextEditorField
from wtforms.widgets.html5 import DateInput as DateWidget

#factory = Type.query.all()

class AddSettingForm(Form):
    name = fields.StringField('Setting Name',validators=[validators.InputRequired()])
    #type = QuerySelectField('setting type',query_factory=factory,validators=[validators.InputRequired()])
    default = fields.StringField('Default Value')
    value = fields.StringField('Setting Value')

class AddSettingTypeForm(Form):
    name = fields.StringField('Setting Type Name',validators=[validators.InputRequired()])
    widget = fields.StringField('Input Widget')

class TestForm(Form):
    title = fields.StringField('Title')
    content = PageDownField('content')

class BaseTemplateForm(Form):
    template = fields.SelectField('base template',validators=[validators.InputRequired()])#,choices=[('a','a'),('b','b'),('c','c')])

class TemplateBodyFieldForm(Form):
    body = CKTextEditorField('body')


class AddBlogForm(Form):
    name = fields.StringField('Blog Name',validators=[validators.InputRequired()])
    title = fields.StringField('Blog Title',validators=[validators.InputRequired()])
    slug = fields.StringField('Url Slug')
    author_id = fields.HiddenField()
    date_added = fields.HiddenField()
    


class AddPageForm(Form):
    date_added = fields.DateField('Publish On:',format="%m-%d-%Y",widget=DateWidget())
    date_end = fields.DateField('Expire On:',format="%m-%d-%Y",validators=[validators.Optional()],widget=DateWidget())
    name = fields.StringField('Page Name',validators=[validators.InputRequired()])
    description = fields.TextAreaField('Description',validators=[validators.Optional()])
    slug = fields.StringField('Page Slug',validators=[validators.InputRequired()])
    short_url = fields.StringField('Url',validators=[validators.Optional()])
    title = fields.StringField('Page Title',validators=[validators.InputRequired()])
    add_to_nav = fields.BooleanField('Add to Navbar')
    add_sidebar = fields.BooleanField('Add Sidebar')
    visible = fields.SelectField(choices=((1,'Publish'),(0,'Draft')))
    meta_title = fields.StringField('Meta Title',validators=[validators.InputRequired()])
    content = CodeMirrorField('Content',language='xml',config={'lineNumbers':'true'})
    template = fields.FormField(BaseTemplateForm,label="Template",separator='_')
    blocks = fields.SelectMultipleField(label="blocks",choices=[('a','a'),('b','b'),('c','c')])
    category = QuerySelectField('category')
    #tags = TagField('Tags')
    use_base_template = fields.BooleanField('Use Base Template')
    base_template =  fields.SelectField('base template',validators=[validators.InputRequired()])
    submit = fields.SubmitField('Save')
