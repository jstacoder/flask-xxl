import datetime
import math

__all__ = ['human_time','date','date_pretty','datetime','pluralize','month_name']

def datetimeformat(value):
    delta = datetime.datetime.now() - value
    if delta.days == 0:
        formatting = 'today'
    elif delta.days < 10:
        formatting = '{0} days ago'.format(delta.days)
    elif delta.days < 20:
        formatting = '{0} weeks ago'.format(int(math.ceil(delta.days/7.0)))
    elif value.year == datetime.datetime.now().year:
        formatting = 'this year, on %d %b'
    else:
        formatting = 'on %b %d %Y'
    return value.strftime(formatting)

def parse_date(date):
    import dateutil.parser as p
    return p.parse(str(date))


def human_time(timestamp):
    d = parse_date(timestamp)
    return datetimeformat(datetime.datetime(d.year,d.month,d.day))

def date(value):
    """Formats datetime object to a yyyy-mm-dd string."""
    value = parse_date(value)
    return value.strftime('%Y-%m-%d')

def date_time_pretty(value):
    """Formats datetime object to a Month dd, yyyy string."""
    value = parse_date(value)
    return value.strftime('%B %d, %Y at %I:%M %P')

def date_pretty(value):
    """Formats datetime object to a Month dd, yyyy string."""
    value = parse_date(value)
    return value.strftime('%h %d, %Y' )


def dt(value):
    """Formats datetime object to a mm-dd-yyyy hh:mm string."""
    value = parse_date(value)
    return value.strftime('%m-%d-%Y %H:%M')


def pluralize(value, one='', many='s'):
    """Returns the plural suffix when needed."""
    value = parse_date(value)
    return one if abs(value) == 1 else many


def month_name(value):
    """Return month name for a month number."""
    value = parse_date(value)
    from calendar import month_name
    return month_name[value.month]

def get_day(value):
    value = parse_date(value)
    return value.day



def split(value,symbol=' '):
    return value.split(symbol)
