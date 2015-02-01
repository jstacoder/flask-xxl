# -*- coding: utf-8 -*-

"""
    basemodels.py
    ~~~~~~~~~~~
"""
from functools import wraps
from flask import current_app
from inflection import underscore, pluralize
from sqlalchemy.ext.declarative import as_declarative, declarative_base, declared_attr
from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.ext.sqlalchemy import SQLAlchemy, _BoundDeclarativeMeta
from sqlalchemy import UniqueConstraint,Column,Integer,Text,String,Date,DateTime,ForeignKey,func,create_engine


echo_sql = lambda: current_app.config.get('SQLALCHEMY_ECHO',False)
get_engine = lambda: create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'],echo=echo_sql())
Session = lambda e: scoped_session(sessionmaker(bind=e))

Model = declarative_base()

# classproperty decorator
class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)
    
class SQLAlchemyMissingException(Exception):
    pass

class ModelDeclarativeMeta(_BoundDeclarativeMeta):
    pass

@as_declarative(name='BaseMixin',metaclass=ModelDeclarativeMeta)
class BaseMixin(object):
    __abstract__ = True
    _session = None
    _e = None

    @classproperty
    def _engine(cls):
        if cls._e is None:
           cls._e = get_engine()
        cls._e.echo = echo_sql()
        return cls._e
        
    @declared_attr
    def id(self):
        return Column(Integer,primary_key=True)

    @classproperty
    def session(cls):
        if cls._session is None:
            cls._session = Session(cls._engine)
        return cls._session()
    
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

    @classproperty 
    def query(cls):
        return cls.session.query(cls)

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
