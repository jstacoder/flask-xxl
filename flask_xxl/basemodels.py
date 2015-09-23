# -*- coding: utf-8 -*-
"""
    basemodels.py
    ~~~~~~~~~~~
"""
import os
from functools import wraps
from werkzeug.local import LocalProxy
from flask import current_app,g
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

from inflection import underscore, pluralize
from sqlalchemy.ext.declarative import as_declarative, declarative_base, declared_attr
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import UniqueConstraint,Column,Integer,Text,String,Date,DateTime,ForeignKey,func,create_engine

# classproperty decorator
class classproperty(object):
    def __init__(self, getter):
        self.getter = getter
    def __get__(self, instance, owner):
        return self.getter(owner)


echo_sql = lambda: os.environ.get('DATABASE_URI') and current_app.config.get('SQLALCHEMY_ECHO',False)
get_engine = lambda: create_engine(os.environ.get('DATABASE_URI') or current_app.config['DATABASE_URI'],echo=echo_sql())

Base = declarative_base()

    
class SQLAlchemyMissingException(Exception):
    pass

class BaseMixin(Base):
    __table_args__ = {
        'extend_existing':True
    }
    __abstract__ = True
    _session = None
    _engine = None
    _query = None
    _meta = None

    def __init__(self,*args,**kwargs):
        super(BaseMixin,self).__init__(*args,**kwargs)
        metadata = BaseMixin.metadata or Base.metadata
        self.metadata = BaseMixin.metadata = metadata

    @classproperty
    def engine(cls):
        if BaseMixin._engine is None:
           BaseMixin._engine = get_engine()
        BaseMixin._engine.echo = echo_sql()
        return BaseMixin._engine
        
    @declared_attr
    def id(self):
        return Column(Integer,primary_key=True)

    @classproperty
    def session(cls):
        if BaseMixin._session is None:
            BaseMixin._session = scoped_session(sessionmaker(bind=cls.engine))()
        return BaseMixin._session
        
    @classproperty
    def query(cls):
        if cls._query is None:
            cls._query = cls.session.query(cls)
        return cls._query
    
    @declared_attr
    def __tablename__(self):
        return underscore(pluralize(self.__name__))
    
    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None
    
    @classmethod
    def get_all(cls):        
        return cls.query.all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self,commit=True,testing=False):
        try:
            self.session.add(self)
            if commit:
                self.session.commit()
        except Exception, e:
            if not testing:
                raise e
            print e.message            
            return False
        return self

    def delete(self, commit=True):
        self.session.delete(self)
        return commit and self.session.commit()

    @property
    def absolute_url(self):
        return self._get_absolute_url()

    def _get_absolute_url(self):
        raise NotImplementedError('need to define _get_absolute_url')

    @classmethod
    def get_all_columns(cls,exclude=['id']):
        if not 'id' in exclude:
            exclude.append('id')
        rtn = []
        for col in cls.__table__.c._all_columns:
            if not col.name in exclude and not col.name.endswith('id'):
                rtn.append((col.name,_clean_name(col.name)))
        for attr in dir(cls):
            if not attr in exclude:
                if not attr in [x[0] for x in rtn]:
                    if not attr.startswith('_') and not attr.endswith('id'):
                        if not callable(getattr(cls,attr)):  
                            rtn.append((attr,_clean_name(attr)))
        return rtn

    
class AuditMixin(object):
    __abstract__ = True

    @declared_attr
    def date_added(self):
        return sq.Column(sq.DateTime,default=dt.now)

    @declared_attr
    def date_modified(self):
        return sq.Column(sq.DateTime,onupdate=dt.now)

def _clean_name(name):
    names = name.split('_')
    if len(names) > 1:
        if len(names) == 2:
            name = names[0].title() + ' ' + names[-1].title()
        else:
            name = names[0].title() + ' {} '.format(' '.join(map(str,names[1:-1]))) + names[-1].title()
    else:
        name = names[0].title()
    return name

class DBObject(object):
    _session = None
    _engine = None
    _metadata = None

    @staticmethod
    def check_ctx():
        return stack.top is not None
    
    @classproperty
    def session(cls):
        sess = cls._session
        if sess is None:
            sess = DBObject._session = scoped_session(sessionmaker(bind=DBObject.engine))
        return sess

    @classproperty
    def engine(cls):
        engine = cls._engine 
        if engine is None:
            engine = cls._engine = cls.check_ctx() and current_app.config.get('DATABASE_URI') or os.environ.get('DATABASE_URI')
        return engine
    
    @classproperty
    def metadata(cls):
        meta = cls._metadata
        if meta is None:
            meta = cls._metadata = BaseMixin.metadata
        meta.bind = meta.bind if meta.bind else cls.engine
        return meta

db = LocalProxy(DBObject)
