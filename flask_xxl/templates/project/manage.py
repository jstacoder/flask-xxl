#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    manage
    ~~~~~~
"""
import subprocess
from flask.ext.script import Shell, Manager, prompt_bool
from app import app
from ext import db

import sqlalchemy_utils as squ
from flask.ext.alembic.cli.script import manager as alembic_manager
manager = Manager(app)


@manager.command
def clean_pyc():
    """Removes all *.pyc files from the project folder"""
    clean_command = "find . -name *.pyc -delete".split()
    subprocess.call(clean_command)


@manager.command
def init_data():
    from imports import (
                    Widget,Article,Page,
                    User,Setting,Type,
                    Template,Tag,Role,
                    Category,Block
    )
    """Fish data for project"""
    if prompt_bool('Do you want to kill your db?'):
        if squ.database_exists(db.engine.url):
            squ.drop_database(db.engine.url)
    try:
        db.drop_all()
    except:
        pass
    try:
        squ.create_database(db.engine.url)
        db.create_all()
    except:
        pass

    user = User.query.filter(User.email=='kyle@level2designs.com').first()
    if user is None:
       user = User(username='Kyle Roux', email='kyle@level2designs.com', password='14wp88')
    user.save()


manager.add_command('shell', Shell(make_context=lambda:{'app': app, 'db': db}))


if __name__ == '__main__':
    manager.add_command('db',alembic_manager)
    app.test_request_context().push()
    from imports import (
                    Widget,Article,Page,
                    User,Setting,Type,
                    Template,Tag,Role,
                    Category,Block
    )
    manager.run()
