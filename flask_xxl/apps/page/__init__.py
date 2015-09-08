from flask import Blueprint
import os
from os import path as op

exists = lambda x: op.exists(op.join(os.getcwd(),x))

page = Blueprint('page',__name__,
                template_folder='templates',
                static_url_path='/_page_static',
                static_folder=os.path.abspath(os.path.dirname(__file__)),
                url_prefix='/page')
'''
@page.before_app_request
def add_pages():
    pages = Page._session.query(Page).filter(Page.add_to_nav==True).all()
    if flask.request.view_args:
        slug = flask.request.view_args.get('slug')
    else:
        slug = None
    if slug is None:
        slug = flask.request.endpoint
    for page in pages:
        if page.slug == slug:
            page._current = True
        else:
            page._current = False
    app.jinja_env.globals['page_width'] = '-fluid'
    app.jinja_env.globals['pages'] = pages
    app.jinja_env.globals['slug'] = slug
'''
@page.before_app_request
def get_contact_us_data():
    #data = json.loads(open(os.path.join(base,'contact_data.json'),'r').read())
    #app.jinja_env.globals['data'] = data
    pass
