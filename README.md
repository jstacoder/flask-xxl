## Flask-XXL  
#### - A best practices approach to creating larger web apps with Flask, in an attempt to make Flask feel like it is as capable, if not more, than __Django__.
this is an amazing program best in the world
[![PyPI version](https://badge.fury.io/py/flaskxxl.svg)](https://badge.fury.io/py/flaskxxl)

[![Get help on Codementor](https://cdn.codementor.io/badges/get_help_github.svg)](https://www.codementor.io/jstacoder)

[![Join the chat at https://gitter.im/jstacoder/flask-xxl](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jstacoder/flask-xxl?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

_to see this in a real world example take a look at my other projects_ [Flask-Cms](https://github.com/jstacoder/flask-cms) or [Flask-Ide](https://github.com/jstacoder/flask-ide)



## What this provides:  

-   Installable blueprints  
    - any blueprints listed in your settings under `BLUEPRINTS`   
    will be imported and registered on your app  
    if that blueprint is a package, any files it contains named `models.py` or `views.py` will be imported as well,   
    so no more need to manualy import your views and models  
    giving odd errors if you dont do it in the exact correct order!!

-   basemodels.py 
    -   with a sqlalchemy compatible BaseMixin class
      - provides many useful CRUD operations, IE: model.save(), model.delete()
      - `BaseMixin` generates `__tablename__` automaticlly
      - `BaseMixin` adds an auto incrementing `id` field, as the primary_key to each model
      - `BaseMixin.session` is current model classes session
      - `BaseMixin.engine` is the current db engine
      - `BaseMixin.query` is the models sqlalchemy query from its session
      - `BaseMixin.get_all()` `->` function to return all of a model
      - `BaseMixin.get(*args,**kwargs)` `->` get single model by attr values, mainly for id=x

-   baseviews.py
    -   with a BaseView class that is subclassed from Flask.views.MethodView to allow easy definition of view responses to get and post requests.
    -   BaseView also has many builtin helpers/imports to speed development, ie: 
      -   BaseView.render() calls:  
      `render_template(BaseView._template,**BaseView._context)`
      easily define either or both in the class variable
      section of the class and then add or change whatever you need to
      ie: maybe based on logic that happens during request processing.   
      for example:            
      ```python
            class ExampleView(BaseView):
                _context = {
                    'some_flag':True,
                }

                def get(self,new_flag=False):
                    if new_flag:
                        self._context['new_flag'] = new_flag
                        self._context['some_flag'] = False
                    return self.render()  
                    
    ```                    
      
   -   `BaseView.redirect(endpoint)`
        is a reimplementation of `flask.helpers.redirect` which allows you to directly enter the
        endpoint, so you dont have to run it through `url_for()` first. 
        
        - `BaseView.get_env()` -> returns the current jinja2_env        
        
        - `BaseView.form_validated()` -> returns true if all forms validate
        
        -   __namespaces imported into BaseView__:
            `BaseView.flash == flask.flash`
            
        
            

-   many builtin template globals(context_processors) to use.
    ie: 

    - `get_block(block_id)` <-- requires use of flask.ext.xxl.apps.blog 
     *   add blocks of html/jinja2/template helpers 
         into the db and access from within templates
         great for things like header navs or sidebar widgets
                
    - `get_icon(icon_name,icon_lib)` <-- requires use of flask.ext.xxl.apps.blog
        - flask.ext.xxl.apps.blog comes with 8 icon librarys!!!  
            * Glyphicon  
            * Font Awesome
            * Mfg_Labs
            * Elusive icons
            * Genericons
            * and more ...   
      
      access any icon anywhere in your templates! even from cms blocks!!!
                
    - `get_model(model_name,blueprint_name)`
        - access any model class from any template (currently only supports sqlalchemy models)
            
    - `get_button(name)`
        - create buttons in the cms and access from within templates

- AppFactory class with many hooks into settings file (makes use of settings file similar to django)
  -   settings like:
    -   CONTEXT_PROCESSORS
    -   TEMPLATE_FILTERS
    -   URL_ROUTE_MODULES
    -   INSTALLED_BLUEPRINTS etc..

- new revamped url routing scheme, use a urls.py file in each blueprint to 
  define the url routes for the blueprint. reference the blueprint and the url
  route module in the settings file to registar onto the app upon instantiation.  

  define routes like this:

  file: urls.py
  ```python
        from blueprint import blueprint
        from .views import ViewName,SecondView

        routes = [
            ((blueprint_name,)
                ('/url',ViewName.as_View('view_name')),
                ('/another',SecondView.as_view('second_view')),
            )
        ]
    ```
    it basicly is like using `app.add_url_rule()` method, you
    just dont have to add `view_func=ViewName.as_view(endpoint)`
    or at least the `view_func=` part.


-   easily start a new project or extend an old one  
    with the flaskxxl-manage.py command line helper tool
    - to start a project from scratch  
      `$ flaskxxl-manage.py start-project`
        
    -   to add to an existing project  
        `$ flaskxxl-manage.py start-blueprint`


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/jstacoder/flask-xxl/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

for more fun checkout the [wiki](https://github.com/jstacoder/flask-xxl/wiki)
