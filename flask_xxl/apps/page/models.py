from basemodels import BaseMixin
import datetime
from ext import db
from flask import url_for

for attr in dir(db):
    globals()[attr] = getattr(db,attr)

class Page(BaseMixin,Model):
    __tablename__ = 'pages'

    name = Column(String(255))
    description = Column(Text)
    template_id = Column(Integer,ForeignKey('templates.id'))
    template = relationship('Template',backref=backref(
                'pages',lazy='dynamic'))
    slug = Column(String(255))
    title = Column(String(255))
    add_to_nav = Column(Boolean,default=False)
    date_added = Column(DateTime,default=datetime.datetime)
    visible = Column(Boolean,default=False)
    meta_title = Column(String(255))
    content = Column(Text)
    use_base_template = Column(Boolean,default=True)
    added_by = relationship('User',backref=backref(
        'pages',lazy='dynamic'))
    user_id = Column(Integer,ForeignKey('users.id'))
    add_sidebar = Column(Boolean,default=False)
    short_url = Column(String(255))

    def __repr__(self):
        if self.name is None:
            rtn = '<Page: Unnamed | {}'.format(self.line_count)
        else:
            rtn = '<Page: {} | {} lines'.format(self.name,self.line_count)
        return rtn


    def _get_page_url(self):
        return url_for('page.pages',slug=self.slug)

    @staticmethod
    def _get_create_url():
        return url_for('admin.add_page')

    @classmethod
    def get_by_slug(cls,slug):
        return cls.query.filter(cls.slug==slug).first()

    def _get_absolute_url(self):
        return url_for('admin.page_view',slug=self.slug)

    def _get_edit_url(self):
        return url_for('admin.edit_page',item_id=int(self.id))

    def _get_edit_content_url(self):
        return url_for('admin.edit_page_content',item_id=int(self.id))

    @property
    def line_count(self):
        try:
            rtn = len(self.content.split('\n'))
        except:
            rtn = 0
        return rtn

    @property
    def template_name(self):
        return self.template.name or ''

    @property
    def block_count(self):
        return self.blocks.count()


class Template(BaseMixin,Model):
    __tablename__ = 'templates'

    name = Column(String(255),nullable=False,unique=True)
    body = Column(UnicodeText)
    filename = Column(String(255))
    imports = Column(String(255))
    base_template = Column(String(255))
    is_base_template = Column(Boolean,default=False)

    def __init__(self,*args,**kwargs):
        self._raw_template = ''
        self._head = ''
        for attr in ['name','body','filename']:
            tmp = kwargs.pop(attr,None)
            if tmp is not None:
                self.__dict__[attr] = attr
        base = kwargs.pop('base_template',None)
        if base is None:
            self.is_base_template = True
        else:
            self.is_base_template = False
            self._add_to_head(self._create_extend(base))
        imports = kwargs.pop('imports',None)
        if imports is not None:
            for f,i in imports:
                self._add_to_head(self._create_import(f,i))
        if self.body:
            self._set_template()

    def _add_to_head(self,itm):
        self._head = self._head + '\n' + itm

    def _create_extend(self,parent):
        return '{% extends "%s" %}' % parent

    def _create_import(self,file_name,import_name,with_context=False):
        fmt = '{% from "%s" import %s %s %}'
        with_context = with_context or ''
        return fmt % (file_name,import_name,with_context)

    def _set_template(self):
        from jinja2 import Template
        self._raw_template = Template(self._head + self.body[:])

    @property
    def block_count(self):
        return len(self._raw_template.blocks)

    @property
    def blocks(self):
        return self._raw_template.blocks.keys()

    def set_body(self,data):
        self.body = data
        self._set_template()
    @property
    def body_body(self):
        return self.body

    @property
    def content(self):
        return self.body[:]

    def _get_edit_url(self):
        return url_for('admin.edit_template',item_id=int(self.id))

    def _get_absolute_url(self):
        return url_for('admin.template_view',name=self.name)

    def __repr_(self):
        if self.name is None:
            rtn = '<Template: Unnamed | {} lines'.format(self.line_count)
        else:
            rtn = '<Template: {} | {} lines'.format(self.name,self.line_count)
        return rtn

    def __str__(self):
        return self.body or ''

    @staticmethod
    def _get_create_url():
        return url_for('admin.add_template')

    @property
    def line_count(self):
        try:
            rtn = len(self.body.split('\n'))
        except:
            rtn = 0
        return rtn


    def get_block_count(self):
        return len(self._raw_template.blocks.keys())


class Block(BaseMixin,Model):
    __tablename__ = 'blocks'

    name = Column(String(255))
    content = Column(Text)

    def set_content(self,data):
        self.content = data

    def render(self):
        return self.content or ''

    def __str__(self):
        s = self.content.split('\n')
        return '<br />'.join(map(str,s))

    def __repr__(self):
        if self.name is None:
            rtn = '<Block: Unnamed | {} lines'.format(self.line_count)
        else:
            rtn = '<block: {} | {} lines'.format(self.name,self.line_count)
        return rtn


    @staticmethod
    def _get_create_url():
        return url_for('admin.add_block')

    def _get_edit_content_url(self):
        return url_for('admin.edit_block_content',item_id=int(self.id))

    def _get_edit_url(self):
        return url_for('admin.edit_block',item_id=int(self.id))

    def _get_absolute_url(self):
        return url_for('admin.block_view',name=self.name)

    @property
    def line_count(self):
        try:
            rtn = len(self.content.split('\n'))
        except:
            rtn = 0
        return rtn


