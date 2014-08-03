from basemodels import BaseMixin
from LoginUtils import check_password, encrypt_password
from ext import db

for attr in dir(db):
    globals()[attr] = getattr(db,attr)


class Setting(BaseMixin,Model):
    __tablename__ = 'settings'

    name = Column(String(255),nullable=False,unique=True)
    setting_type_id = Column(Integer,ForeignKey('types.id'))
    setting_type = relationship('Type',backref=backref(
        'settings',lazy='dynamic'))
    default = Column(String(255))
    value = Column(String(255))

    @property
    def widget(self):
        if self.type:
            return self.type.widgets
        else:
            return ''

class Type(BaseMixin,Model):
    __tablename__ = 'types'

    name = Column(String(255),nullable=False)
    widgets = relationship('Widget',backref=backref(
        'type'),lazy='dynamic')
    html = Column(Text)
    field_type = Column(String(255))
    required = Column(Boolean,default=False)
    data_type = Column(String(255))

    def __repr__(self):
        return self.name or ''

class Widget(BaseMixin,db.Model):
    __tablename__ = 'widgets'

    name = Column(String(255),nullable=False)
    title = Column(String(255))
    content = Column(Text,nullable=False)
    type_id = Column(Integer,ForeignKey('types.id'))

    def __repr__(self):
        return self.name

