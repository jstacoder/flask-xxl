from flask import Blueprint

page = Blueprint('page',__name__,
                template_folder='templates',
                url_prefix='/page')


from views import *
