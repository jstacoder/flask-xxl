# -*- coding: utf-8 -*-
"""
    context_processors.py
"""

from inflection import camelize

def get_model(model_name, blueprint=None):
    class_name = camelize(
        model_name
    )
    return __import__(
        blueprint or model_name.lower() + 
        '.models', globals(), locals(),
        fromlist=[],
    ).models.__dict__[class_name]


def add_get_model():
    return {'get_model': get_model}
