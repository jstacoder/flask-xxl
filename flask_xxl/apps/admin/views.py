# -*- coding: utf-8 -*-

"""
    admin.views

    Administrative Views
"""
import os
from ..auth.utils import login_required
from datetime import datetime
from flask_wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from ...baseviews import BaseView,ModelView
from ..admin import admin
from flask import request,session,flash
from .forms import AddBlogForm

class FakePage(object):
    link = None
    text = None

    def __init__(self,page):
        self.text = page.title
        self.link = page._get_page_url()

class AdminDashboardView(BaseView):
    _template = 'dashboard.html'

    decorators = [login_required]

    def get(self):

        return self.render()

class AdminSiteSettingsView(BaseView):
    _template = 'settings.html'

    decorators = [login_required]

    def get(self):
        from admin.forms import SiteSettingsForm
        from admin.models import SiteSetting
        settings = SiteSettings.query.all()
        self._form = SiteSettingsForm(obj=settings)



class AdminPageView(BaseView):
    _template = 'add.html'
    _context = {
                    'form_args':
            {
                'heading':'Add CMS Page',
            }
    }

    decorators = [login_required]

    def get(self):
        if not 'content' in request.endpoint:
            from ..page.models import Page
            from wtforms import FormField
            from .forms import BaseTemplateForm
            from ..auth.models import User
            from ..page.models import Template
            self._context['choices'] = [(x,x.name) for x in Template.query.all()]
            from ext import db
            form = model_form(Page,db.session,base_class=Form,exclude=['date_added','added_by'])
            class PageForm(form):
                template = FormField(BaseTemplateForm)
                def __init__(self,*args,**kwargs):
                    if 'prefix' in kwargs:
                        kwargs.pop('prefix')
                    super(PageForm,self).__init__(*args,**kwargs)

            self._form = PageForm(prefix=False)
        else:
            from ..page.forms import EditContentForm
            from ..auth.models import User
            self._form = EditContentForm
        return self.render()

    def post(self):
        if 'content' in request.endpoint:
            session['content'] = request.form['content'][:]
            return self.redirect('admin.add_page')
        else:
            from ..auth.models import User
            from .forms import BaseTemplateForm
            from ..page.models import Template
            from ..page.models import Page
            from wtforms import FormField
            from ...ext import db
            self._context['choices'] = [(x,x.name) for x in Template.query.all()]
            form = model_form(Page,db.session,base_class=Form,exclude=['date_added','added_by'])
            class PageForm(form):
                template = FormField(BaseTemplateForm)

                def _get_template_id(self,template_name):
                    from page.models import Template
                    t = Template.query.filter(Template.name==template_name).first()
                    if t:
                        return t.id
                    return None

                def __init__(self,*args,**kwargs):
                    if 'prefix' in kwargs:
                        kwargs.pop('prefix')
                    super(PageForm,self).__init__(*args,**kwargs)
                def populate_obj(self,obj):
                    for name,field in self._fields.items():
                        if name == 'template':
                            obj.template_id = self._get_template_id(field.template.data)
                            self._fields.pop(name)
                    super(PageForm,self).populate_obj(obj)

            self._form = PageForm(request.form)
            page = Page()
            self._form.populate_obj(page)
            if 'content' in session:
                page.content = session.pop('content',None)
            page.save()
            flash('Successfully created cms page: {}'.format(page.name))
            return self.redirect('admin.pages')
        return self.render()




class AdminTemplateView(BaseView):
    _template = 'add.html'
    _context = {'mce':True,
                    'form_args':
            {
                'heading':'Add a Template',
            }
    }

    decorators = [login_required]

    def get(self):
        from auth.models import User
        from page.models import Template
        from wtforms import FormField
        from admin.forms import TemplateBodyFieldForm
        from ext import db
        AddTemplateForm = model_form(Template,db.session,base_class=Form,exclude=['blocks','pages','body'])
        class TemplateForm(AddTemplateForm):
            body = FormField(TemplateBodyFieldForm)

        self._form = TemplateForm
        return self.render()

    def post(self):
        from page.models import Template
        from auth.models import User
        from ext import db
        self._form = model_form(Template,db.session,base_class=Form,exclude=['blocks','pages','body'])(request.form)
        if self._form.validate():
            template = Template()
            self._form.populate_obj(template)
            template.save()
            filename = template.filename
            if template.body is not None:
                body = template.body[:]
            else:
                body = ''
            from settings import BaseConfig
            import os
            templatedir = os.path.join(BaseConfig.ROOT_PATH,'templates')
            os.system('touch {}'.format(os.path.join(templatedir,filename)))
            fp = open(os.path.join(templatedir,filename),'w')
            fp.write(body+'\n')
            fp.close()
            flash('you have created a new template named: {}'.format(template.name))
            return self.redirect('admin.templates')
        else:
            flash('You need to give the template a name')
        return self.render()

    @staticmethod
    @admin.before_app_request
    def check_templates():
        from ..page.models import Template
        from ..auth.models import User
        from flask import current_app
        templates = Template.query.all()
        template_dir = current_app.config['ROOT_PATH'] + '/' + 'templates'
        if not os.path.exists(template_dir):
            os.mkdir(template_dir)
        names = [t.name for t in templates]
        for t in os.listdir(template_dir):
            if not t in names:
                temp = Template()
                temp.name = t
                temp.filename = os.path.join(template_dir,t)
                temp.body = open(os.path.join(template_dir,t),'r').read()
                temp.save()

class AdminBlockView(BaseView):
    _template = 'add.html'
    _context = {'mce':True,
                    'form_args':
            {
                'heading':'Add CMS Block',
            }
    }

    decorators = [login_required]

    def get(self):
        if not 'content' in request.endpoint:
            from auth.models import User
            from page.models import Block
            from ext import db
            AddBlockForm = model_form(Block,db.session,base_class=Form)
            self._form = AddBlockForm
        else:
            content = session.pop('content','')
            from page.forms import EditContentForm
            self._form = EditContentForm
            self._form.content.data = content
        return self.render()

    def post(self):
        if 'content' in request.endpoint:
            session['content'] = request.form['content'][:]
            return self.redirect('admin.add_block')
        else:
            content = session.pop('content',None)
            from page.models import Block
            from ext import db
            AddBlockForm = model_form(Block,db.session,base_class=Form)
            self._form = AddBlockForm(request.form)
            block = Block()
            self._form.populate_obj(block)
            if 'content' in session:
                block.content = content
            block.save()
            flash('Successfully created cms block: {}'.format(block.name))
            return self.redirect('admin.blocks')
        return self.render()
    @staticmethod
    @admin.before_app_request
    def check_blocks():
        from ..page.models import Block as model
        from ..auth.models import User
        objs = model.query.all()
        from flask import current_app as app
        block_dir = app.config['ROOT_PATH'] + '/' + 'blocks'
        if not os.path.exists(block_dir):
            os.mkdir(block_dir)
        names = [o.name for o in objs]
        for o in os.listdir(block_dir):
            if not o in names:
                if not o.startswith('_'):
                    temp = model()
                    temp.name = o
                    temp.content = ''.join(map(str,open(os.path.join(block_dir,o),'r').readlines()))
                    temp.save()

class AdminCMSListView(BaseView):
    _template = 'list.html'
    _context = {}

    decorators = [login_required]

    def get(self):
        from settings import BaseConfig
        from page.models import Page,Block,Template
        from auth.models import User
        pp = BaseConfig.ADMIN_PER_PAGE
        if 'users' in request.endpoint:
            obj= User
        if 'page' in request.endpoint:
            obj = Page
        if 'block' in request.endpoint:
            obj = Block
        if 'template' in request.endpoint:
            obj = Template
        objs = obj.query.all()
        if len(objs) > pp:
            return self.redirect('admin.page_{}'.format(obj.__name__.lower()),page_num=1)
        exclude = ['password','templates','pages','id','body','content',
                    'query','metadata','template','blocks','body_body',
                    'template_id','use_base_template','absolute_url','body-body',
                    'added_by','body_body','articles','role_id','_pw_hash',
                    'is_unknown']
        headings = obj.get_all_columns(exclude)
        self._context['objs'] = objs
        self._context['columns'] = [x[0] for x in headings]
        self._context['headings'] = [x[1] for x in headings]
        return self.render()


class AdminListPageView(BaseView):
    _template = 'list.html'

    decorators = [login_required]

    def get(self,page_num=1):
        from admin.utils import Pagination
        from settings import BaseConfig
        pp = BaseConfig.ADMIN_PER_PAGE
        endpoint = request.endpoint
        if '_users' in endpoint:
            from auth.models import User
        if '_page' in endpoint:
            from page.models import Page as model
        elif '_template' in endpoint:
            from page.models import Template as model
        else:
            from page.models import Block as model
        p = Pagination(model,page_num)
        self._context['objs'] = p._objs
        self._context['pagination'] = p
        exclude = ['password','templates','pages','id','body','content',
                    'query','metadata','template','blocks','body-body',
                    'template_id','use_base_template','absolute_url','body_body',
                    'added_by','articles','role_id','_pw_hash','is_unknown']
        headings = p._objs[0].get_all_columns(exclude)
        self._context['columns'] = [x[0] for x in headings]
        self._context['headings'] = [x[1] for x in headings]
        self._context['use_codemirror'] = True
        return self.render()





class AdminDetailView(BaseView):

    decorators = [login_required]

    def get(self,slug=None,name=None):
        endpoint = request.endpoint[:]
        if 'page' in request.endpoint:
            self._template = 'view_page.html'
        if 'block' in request.endpoint:
            self._template = 'view_block.html'
        if 'template' in request.endpoint:
            self._template = 'view_template.html'
        if 'page' in endpoint:
            from page.models import Page
            obj = Page.query.filter(Page.slug==slug).first()
        if 'block' in endpoint:
            from page.models import Block
            obj = Block.query.filter(Block.name==name).first()
        if 'template' in endpoint:
            from page.models import Template
            obj = Template.query.filter(Template.name==name).first()

        self._context['obj'] = obj
        self._context['lines'] = obj.content.split('\n') or obj.body.split('\n')
        return self.render()



class AdminEditView(BaseView):
    _template = 'add.html'
    _context = {
                    'form_args':
            {
                'heading':'Edit CMS Item',
            }
    }

    decorators = [login_required]

    def get(self,item_id=None):
        from auth.models import User
        from ext import db
        if 'page' in request.endpoint:
            from page.models import Page
            page = Page.get_by_id(item_id)
            if not 'content' in request.endpoint:
                self._form = model_form(Page,db.session,base_class=Form,exclude=['added_by','date_added'])
                self._context['obj'] = page
            else:
                from page.forms import EditContentForm
                self._form = EditContentForm
            self._form_obj = page
        elif 'block' in request.endpoint:
            from page.models import Block
            block = Block.get_by_id(item_id)
            if not 'content' in request.endpoint:
                self._form = model_form(Block,db.session,base_class=Form,exclude=['templates','pages'])
                self._context['obj'] = block
            else:
                from page.forms import EditContentForm
                self._form = EditContentForm
            self._form_obj = block
        else:
            from admin.forms import TemplateBodyFieldForm
            from wtforms import FormField
            from page.models import Template
            template = Template.get_by_id(item_id)
            form = model_form(Template,db.session,base_class=Form,exclude=['pages','blocks','filename','body'])

            class TemplateForm(form):
                body = FormField(TemplateBodyFieldForm,separator='_')
            self._form = TemplateForm
            self._context['obj'] = template
            self._form_obj = template
        return self.render()

    def post(self,item_id=None):
        from ext import db
        from auth.models import User
        if 'content' in request.endpoint:
            session['content'] = request.form['content'][:]
            return self.redirect('admin.edit_{}'.format(request.url.split('/')[-3]),item_id='{}'.format(request.url.split('/')[-1]))
        else:
            if 'page' in request.endpoint:
                from page.models import Page as model
                needs_content = True
                msg = 'cms page'
                redirect = 'pages'
                exclude = ['added_by','date_added']
            if 'block' in request.endpoint:
                from page.models import Block as model
                needs_content = True
                msg = 'cms block'
                redirect = 'blocks'
                exclude = ['templates','pages']
            if 'template' in request.endpoint:
                from page.models import Template as model
                needs_content = False
                msg = 'template'
                redirect = 'templates'
                exclude = ['pages','blocks']
            self._form = model_form(model,db.session,base_class=Form,exclude=exclude)(request.form)
            obj = model.query.filter(model.id==item_id).first()
            self._form.populate_obj(obj)
            if needs_content:
                if 'content' in session:
                    obj.content = session.pop('content',None)
            obj.update()
            flash('Successfully updated {}: {}'.format(msg,obj.name))
            return self.redirect('admin.{}'.format(redirect))

class TestView(BaseView):
    _template = 'add.html'
    _form = None
    _context = {}

    def get(self):
        from admin.forms import TestForm
        self._form = TestForm
        self._form._has_pagedown = False
        self._context['url_link'] = 'admin.test'
        return self.render()



class PageListView(BaseView):
    _template = 'list_pages.html'
    _context = {}

    def get(self):
        from page.models import Page
        pages = [FakePage(page) for page in Page.query.all()]
        self._context['page_list'] = pages
        return self.render()


class AdminSettingsView(BaseView):
    _template = 'settings.html'
    _form = None # uses AddSettingForm and SettingForm
    _context = {}

    def get(self):
        self._get_settings_widgets()
        return self.render()

    def _get_settings_widgets(self):
        from .models import Setting
        self._context['widgets'] = [x.widget for x in Setting.query.all()]


class AdminAddCategoryView(BaseView):
    _template = 'add.html'
    _form = None
    _context = {}
    _form_heading = 'Add a Category'
   
    decorators = [login_required]

    def get(self):
        self._context['form_args'] = {'heading':self._form_heading}
        return self.render()

    def post(self):
        self._context['form_args'] = {'heading':self._form_heading}
        self._form = self._form(request.form)
        if self._form.validate():
            class Category(object):
                def save(self):
                    pass
            c = None#Category.query.filter(Category.name==self._form.name.data).first()
            if c is None:
                c = Category()
                c.name = self._form.name.data
                c.description = self._form.description.data
                #c.save()
                self.flash('You added category: {}'.format(c.name),'success')
            else:
                self.flash('There is already a category by that name, try again','danger')
        return self.render()

class AdminBlogView(BaseView):
    _template = 'blog_settings.html'
    _form = None
    _context = {}

    def get(self,blog_id=None):
        return self.render()

class AdminAddBlogView(BaseView):
    _template = 'add.html'
    _form = None
    _context = {}

    decorators = [login_required]

    def get(self):
        self._form = AddBlogForm(author_id=session.get('user_id'),date_added=datetime.now())
        return self.render()

    def post(self):
        self._form = AddBlogForm(request.form)
        if self._form.validate():
            class Blog(object):
                def save(self):
                    pass
            blog = Blog()
            blog.name = self._form.name.data
            blog.date_added = self._form.date_added.data
            blog.title = self._form.title.data
            blog.slug = self._form.slug.data
            author_id = self._form.author_id.data
            category = self._form.category.data
            blog.save()
        return self.redirect('blog.list')





    
from flask import jsonify
@admin.route('/add/tst')
def tst():
    num = request.args.get('num',None)
    if num is None:
        res = {'val':'none'}
    else:
        res = {'num':num*2}
    return jsonify(result=res)



