

def is_page(obj):
    return obj.__class__.__name__ == 'Page'


def add_is_page():
    return {'is_page':is_page}
