from flask import Blueprint

auth = Blueprint('auth',__name__,
                 template_folder='templates',
                 url_prefix='/auth')
                                    

try:
    from views import *
except ImportError, e:
    print 'Could not load {} '.format(e)


