# -*- coding: utf-8 -*-

"""
    app.py
    ~~~~~~

    app initalization
"""
from main import AppFactory
from settings import DevelopmentConfig

app = AppFactory(DevelopmentConfig).get_app(__name__)


