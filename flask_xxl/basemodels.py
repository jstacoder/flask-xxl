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

get_engine = lambda: create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
Session = lambda: scoped_session(sessionmaker(bind=get_engine()))
echo_sql = lambda: current_app.config.get('SQLALCHEMY_ECHO',False)
Model = declarative_base()


class SQLAlchemyMissingException(Exception):
    pass

class ModelDeclarativeMeta(_BoundDeclarativeMeta):
    pass

@as_declarative(name='BaseMixin',metaclass=ModelDeclarativeMeta)
class BaseMixin(Model):
    __abstract__ = True
    _session = None

    @property
    def _engine(self):
        self._e = get_engine()
        self._e.echo = echo_sql()
        return self._e
        

    @declared_attr
    def id(self):
        return Column(Integer,primary_key=True)

    @classmethod
    def get_session(cls):
        if cls._session is None:
            cls._session = Session()
        return cls._session

    @staticmethod
    def make_table_name(name):
        return underscore(pluralize(name))
    
    @declared_attr
    def __tablename__(self):
        return BaseMixin.make_table_name(self.__name__)
    
    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query().get(int(id))
        return None
    
    @classmethod
    def get_all(cls):
        return cls.query().all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self,commit=True):
        try:
            session = self.__class__.get_session()
            session.add(self)
            if commit:
                session.commit()
        except:
            return False
        return self

    def delete(self, commit=True):
        session = self.__class__.get_session()
        session.delete(self)
        return commit and session.commit()

    @classmethod
    def query(cls):
        return cls.get_session().query(cls)

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
        for col in cls.__table__.c._all_cols:
            if not col.name in exclude and not col.name.endswith('id'):
                rtn.append((col.name,_clean_name(col.name)))
        for attr in dir(cls):
            if not attr in exclude:
                if not attr in [x[0] for x in rtn]:
                    if not attr.startswith('_') and not attr.endswith('id'):
                        if not callable(getattr(cls,attr)):  
                            rtn.append((attr,_clean_name(attr)))
        return rtn

    
    
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
