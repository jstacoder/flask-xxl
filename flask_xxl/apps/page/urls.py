from . import page
from .views import ContactFormView,PageSlugView,PagesView,AddPageView

routes = [
    (
        (page),
            ('/',PagesView.as_view('page_list')),
            ('/<slug>',PageSlugView.as_view('page')),
            ('/add_page',AddPageView.as_view('add_page')),
            ('/contact-us',ContactFormView.as_view('contact_us')),
    )
]
