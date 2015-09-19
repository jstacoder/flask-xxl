from . import page
from .views import ContactFormView,PageSlugView,PagesView,AddPageView

routes = [
    (
        (page),
            ('/','page_list',PagesView),
            ('/<slug>','page',PageSlugView),
            ('/add_page','add_page',AddPageView),
            ('/contact-us','contact_us',ContactFormView),
    )
]
