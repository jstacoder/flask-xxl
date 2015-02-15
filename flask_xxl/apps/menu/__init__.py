from flask import Blueprint,request,current_app

menu = Blueprint('menu',__name__,
                template_folder='',
                url_prefix="menu")
                                    


from . import views
from . import models


@menu.before_app_request
def add_menu_context():
    if not 'static' in request.path and not 'templates' in request.path:
        links = models.MenuLink.query.all()
        for link in links:
            link.active = False
            if request.endpoint == link.endpoint:
                link.active = True
            link.save()
        current_app.jinja_env.globals['nav_links'] = links

