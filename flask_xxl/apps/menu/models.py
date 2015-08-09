from ...basemodels import BaseMixin
import sqlalchemy as sa

class Menu(BaseMixin):

    name = sa.Column(sa.String(255),unique=True)
    

class MenuLink(BaseMixin):

    name = sa.Column(sa.String(255),nullable=False)
    menu = sa.orm.relationship('Menu',backref=sa.orm.backref('links',lazy='dynamic'))
    menu_id = sa.Column(sa.Integer,sa.ForeignKey('menus.id'))
    text = sa.Column(sa.String(255))
    endpoint = sa.Column(sa.String(255))





