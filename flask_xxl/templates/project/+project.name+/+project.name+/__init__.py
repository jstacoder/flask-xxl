from flask import Blueprint


{{{ project.name.lower() }}} = Blueprint('{{{ project.name.lower() }}}',__name__,
                                template_folder='templates',url_prefix='/')


from .views import *
from .models import *
