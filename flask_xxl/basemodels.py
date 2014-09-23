# -*- coding: utf-8 -*-

"""
    basemodels.py
    ~~~~~~~~~~~
"""
from flask import current_app
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from flask.ext.sqlalchemy import SQLAlchemy, _BoundDeclarativeMeta, _QueryProperty, sessionmaker

class SQLAlchemyMissingException(Exception):
    pass

try:
    db = current_app.extensions['sqlalchemy'].db
except AttributeError, e:
    raise SQLAlchemyMissingException('Need sqlalchemy installed to use basemodel')


class ModelDeclarativeMeta(_BoundDeclarativeMeta):
    pass

@as_declarative(name='Model',metaclass=ModelDeclarativeMeta)
class BaseMixin(object):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer,db.Sequence('user_id_seq'),primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None
    
    @property
    def session(self):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        try:
            self.session.add(self)
            if commit:
                self.session.commit()
        except:
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
