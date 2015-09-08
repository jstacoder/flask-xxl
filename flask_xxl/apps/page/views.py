from flask_xxl.baseviews import BaseView,ModelAPIView
import flask
from . import page
from .forms import TestForm,ContactUsForm
from .models import Page


#class TestView(ModelAPIView):
#    _model = Page

class ContactFormView(BaseView):
    _template = 'contact.html'
    _form = ContactUsForm
    _context = {}

    def get(self):
        return self.render()

    def post(self):
        return self.render()

class PageSlugView(BaseView):
    _template = 'page.html'
    _context = {}

    def get(self,slug):
        file_name = None
        if slug.endswith('.html'):
            # first try to load the html file
            if slug in page.jinja_loader.list_templates():
                file_name = slug
            else:
                slug = slug.split('.html')[0]
                try:
                    url = flask.url_for('page.'+slug)
                    return self.redirect(url)
                except:
                    pass
        test = TestForm()
        content = ''
        page_name = ''
        if '.html' in slug:
            slug = slug.split('.html')[0]
        page = Page._session.query(Page).filter(Page.slug==slug).all()
        if page is not None:
            if type(page) == list and len(page) != 0:
                page = page[0]
            content = page.body_content
            template_file = page.template_file if getattr(page,'template_file',False) and os.path.exists(page.template_file) else page.DEFAULT_TEMPLATE
            page_name = page.name
            title = page.title
            meta_title = page.meta_title
        elif file_name is not None:
            template_file = file_name
            title = slug
            meta_title = slug
        else:
            template_file = slug + '.html'
            title = slug
            meta_title = slug
        self._template = template_file
        self._context['content'] = content
        self._context['page_title'] = title
        self._context['page_name'] = page_name
        self._context['test'] = test
        return self.render()


class AddPageView(BaseView):
    pass

class PagesView(BaseView):
    pass

'''
admin_required = ''

class BasePageView(BaseView):
    _template = ''
    _context = {}
    _base_template = 'aabout.html'
    _parent_template = None

    def render(self):
        return render_template_string(self._template,**self._context)

    def get(self,slug):
        from auth.models import User
        from page.models import Page
        self._page = Page.get_by_slug(slug)
        self.frontend_nav()
        self._context['content'] = self._page.content
        if self._page.use_base_template:
            if self._page.template is not None:
                self._base_template = self._page.body
            self._process_base_template()

    def post(self,slug):
        from auth.models import User
        from page.models import Page
        self._page = Page.get_by_slug(slug)
        self.frontend_nav()
        self._context['content'] = self._page.content
        if self._page.use_base_template:
            if self._page.template is not None:
                self._base_template = self._page.body
            self._process_base_template()

    def _process_base_template(self):
        self._template = "{{template}}"
        self._template = render_template_string(self._template,template=self._base_template)
        self._template =  "{% extends '" + self._template + "' %}<br />{% block body %}{% endblock body %}<br />"

    def frontend_nav(self):
        self._setup_nav()

    def _setup_sidebar(self):
        if self._page.add_to_sidebar:
            sidebar_data = []
            pages = self._page.query.all()
            for page in pages:
                if page.add_to_sidebar:
                    sidebar_data.append(
                        ((page.name,'pages.page',dict(slug=page.slug)))
                    )
            #self._context['sidebar_data'] = ('Title',sidebar_data)

    def _setup_nav(self):
        self._context['nav_links'] = []
        pages = self._page.query.all()
        for page in pages:
            if page.add_to_nav:
                self._context['nav_links'].append(
                        (('page.pages',dict(slug=page.slug)),'{}'.format(page.name))
                )
        self._context['nav_title'] = '{}'.format(self._page.title)
        #self._setup_sidebar()


class PagesView(BasePageView):

    def get(self,slug):
        super(PagesView,self).get(slug)
        #blocks = self._page.blocks.all()
        #self._page.template.process_blocks(blocks)
        return self.render()

    def post(self,slug):
        super(PagesView,self).post(slug)
        data = request.form.get('content')
        if data != self._page.content:
            self._page.content = data
            self._page.update()
        return self.render()


class AddPageView(BaseView):

    def get(self):
        from .models import Page
        from blog.models import Tag
        data = dict(
            date_added=request.args.get('date_added',None),
            date_end=request.args.get('date_end',None),
            name=request.args.get('name',None),
            description=request.args.get('description',None),
            slug=request.args.get('slug',None),
            short_url=request.args.get('short_url',None),
            title=request.args.get('title',None),
            add_to_nav=request.args.get('add_to_nav',None),
            add_sidebar=request.args.get('add_sidebar',None),
            visible=request.args.get('visible',None),
            meta_title=request.args.get('meta_title',None),
            content=request.args.get('content',None),
            template=request.args.get('template',None),
            category=request.args.get('category',None),
            tags=request.args.get('tags',None),
            use_base_template=request.args.get('use_base_template',None),
        )
        p = Page.query.filter(Page.name==data['name']).first()
        if p is not None:
            res = 0
        else:
            tags = [x.name for x in Tag.query.all()]
            for tag in data['tags']:
                if not tag in tags:
                    t = Tag()
                    t.name = tag
                    t.save()
            p = Page()
            p.name = data.get('name')
            p.date_added = data.get('date_added')
            p.date_end = data.get('date_end',None)
            p.description = data.get('description',None)
            p.slug = data.get('slug',None)
            p.short_url = data.get('short_url',None)
            p.title = data.get('title',None)
            nav = data.get('add_to_nav',1)
            if str(nav).lower() == 'y':
                nav = 1
            else:
                nav = 0
            p.add_to_nav = nav
            sidebar = data.get('add_sidebar',0)
            if str(sidebar).lower() == 'y':
                sidebar = 1
            else:
                sidebar = 0
            p.add_sidebar = sidebar
            p.visible = data.get('visible',None)
            p.meta_title = data.get('meta_title',None)
            p.content = data.get('content',None)
            p.template = data.get('template',None)
            p.category = data.get('category',None)
            p.tags = data.get('tags',None)
            p.use_base_template = data.get('use_base_template',None)
            p.save()
            res = 1
        return jsonify(result=res,content=data['content'])
'''
