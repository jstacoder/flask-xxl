import sqlalchemy as sa
from ...basemodels import BaseMixin
from LoginUtils import check_password, encrypt_password
from ...baseviews import is_verbose


if is_verbose():
    print 'importing flask_xxl.apps.admin.models as ',__name__


class Setting(BaseMixin):

    name = sa.Column(sa.String(255),nullable=False,unique=True)
    setting_type_id = sa.Column(sa.Integer,sa.ForeignKey('types.id'))
    setting_type = sa.orm.relationship('Type',backref=sa.orm.backref(
        'settings',lazy='dynamic'))
    default = sa.Column(sa.String(255))
    value = sa.Column(sa.String(255))

    @property
    def widget(self):
        if self.type:
            return self.type.widgets
        else:
            return ''

class Type(BaseMixin):

    name = sa.Column(sa.String(255),nullable=False)
    widgets = sa.orm.relationship('Widget',backref=sa.orm.backref(
        'type'),lazy='dynamic')
    html = sa.Column(sa.Text)
    field_type = sa.Column(sa.String(255))
    required = sa.Column(sa.Boolean,default=False)
    data_type = sa.Column(sa.String(255))

    def __repr__(self):
        return self.name or ''

class Widget(BaseMixin):

    name = sa.Column(sa.String(255),nullable=False)
    title = sa.Column(sa.String(255))
    content = sa.Column(sa.Text,nullable=False)
    type_id = sa.Column(sa.Integer,sa.ForeignKey('types.id'))

    def __repr__(self):
        return self.name

