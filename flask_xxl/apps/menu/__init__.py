from flask import Blueprint

menu = Blueprint('menu',__name__,
                template_folder='',
                url_prefix="menu")
                                    

from views import *
