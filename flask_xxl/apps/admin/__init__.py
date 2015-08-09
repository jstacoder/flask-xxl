# -*- coding: utf-8 -*-
from flask import Blueprint


admin = Blueprint('admin', __name__,
                 template_folder='templates',
                 url_prefix='/admin')


