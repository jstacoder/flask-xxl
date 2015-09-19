import flask
import json
import os
import sqlalchemy as sq
from sqlalchemy import orm
sa = sq
import datetime as dt
from flask_xxl.basemodels import AuditMixin,BaseMixin as Model
#try:
#    from ext import db as Model
#except ImportError:
#    import sys
#    print 'the flask blueprint flask_xxl.apps.page needs a database configured as db in the ext module to work correctley'
#    sys.exit(1)

app_base_dir = os.path.abspath(os.path.dirname(__file__))

class Template(Model):
    name = sq.Column(sq.String(255))

class Block(Model):
    name = sq.Column(sq.String(255))

class Page(Model):

    __tablename__ = 'pages'

    DEFAULT_TEMPLATE = 'page.html'

    id = sq.Column(sq.Integer,primary_key=True)

    parent_id = sa.Column(sa.Integer,sa.ForeignKey('pages.id'))

    children = orm.relationship('Page',backref=orm.backref(
            'parent',remote_side=[id]),lazy='dynamic',primaryjoin='Page.id==Page.parent_id',
             cascade='all,delete-orphan')
    title = sq.Column(sq.String(255),unique=True,nullable=False)
    keywords = sq.Column(sq.Text)
    slug = sq.Column(sq.String(255),unique=True,
            nullable=False)
    template_file = sq.Column(sq.String(255),
            nullable=False,default=DEFAULT_TEMPLATE)
    meta_title = sa.Column(sa.String(255))
    add_right_sidebar = sq.Column(sq.Boolean,default=False)
    add_left_sidebar = sq.Column(sq.Boolean,default=False)
    add_to_nav = sq.Column(sq.Boolean,default=False)
    body_content = sq.Column(sq.Text)

    _current = False

    @property
    def has_children(self):
        return bool(any(self.children))

    def is_parent_to(self,page=False):
        if page:
            return page.id == self.parent.id
        return self.has_children

    def is_child_of(self,page=None):
        if page:
            return page in self.children
        return self.parent is not None

    def add_child(self,page):
        # dont reference any page twice
        if not page in self.children:
            # dont refrence parent
            if self.parent and self.parent.id != page.id:
                self.children.append(page)
                self.save()

    @property
    def navlink(self):
        return (self.title,self.get_absolute_url())

    def get_absolute_url(self):
        return flask.url_for('.page',slug=self.slug)

    @classmethod
    def get_by_slug(cls,slug):
        return cls.query().filter(Page.slug==slug).first()

    @classmethod
    def get_page_count(cls):
        return cls.query().count()

    def __repr__(self):
        return '<{}: #{}-{}'.format(self.__class__.__name__,self.id,self.slug)

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        return self.title


class Category(Model):

    name = sa.Column(sa.String(255),nullable=False,unique=True)
    description = sa.Column(sa.Text)

    def __unicode__(self):
        return self.name
