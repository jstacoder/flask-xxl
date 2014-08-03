from flask import Markup
try:
    from markdown2 import markdown as md2
except ImportError:
    from markdown import markdown as md2
# Jinja

def date(value):
    """Formats datetime object to a yyyy-mm-dd string."""
    return value.strftime('%Y-%m-%d')


def date_pretty(value):
    """Formats datetime object to a Month dd, yyyy string."""
    return value.strftime('%B %d, %Y')


def datetime(value):
    """Formats datetime object to a mm-dd-yyyy hh:mm string."""
    return value.strftime('%m-%d-%Y %H:%M')


def pluralize(value, one='', many='s'):
    """Returns the plural suffix when needed."""
    return one if abs(value) == 1 else many


def month_name(value):
    """Return month name for a month number."""
    from calendar import month_name
    return month_name[value]


def markdown(value):
    """Convert plain text to HTML."""
    extras = ['fenced-code-blocks', 'wiki-tables','attr_list',
              'fenced-code','def-list','tables','extras','meta',
              'nl2br','smart_lists','toc','markdown_checklist.extension']
    return Markup(md2(value, extras=extras))

