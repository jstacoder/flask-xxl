from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models



if not app.debug:
    import os
    import logging

    from logging import Formatter, FileHandler
    from config import basedir

    file_handler = FileHandler(os.path.join(basedir,'error.log'))
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s '
'[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')