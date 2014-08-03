from basemodels import BaseMixin
from ext import db

#import sqlalchemy to global namespace
for attr in dir(db):
    if not attr.startswith('_'):
        globals()[attr] = getattr(db,attr)


class Menu(BaseMixin,Model):
    name = Column(String(255))


