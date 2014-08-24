#__Flask-XXL__

-----------

###__Contents__:

1. overview
2. getting started
3. the settings file 
    * INSTALLED_BLUEPRINTS
    * TEMPLATE_FILTERS 
    * CONTEXT_PROCESSORS
    * ROUTE_MODULES
    * TEMPLATE_LOADERS
    * EXTRA_TEMPLATE_DIRS_
4. Flask, python and MTV
5. Views - _part1_ _begining_
6. Templates - _part1_ _begining_
7. models
8. Templates - _Advanced_
9. Widgets
10. Extending
11. Etc.....

----------------

##Ch.1 - Overview

====================

Flasks creator had the idea, that Django was somewhat of an elephant,(they do say so themselves).
And Who needs an elephant? Well I say there are plenty of cases to use an elephant, but why does 
it have to be Django? I purpose to use flask for the same monumental tasks for which we would 
normally look to somthing bigger. Flask by design is a small framework, it is very good at
being a light, agile framework to build upon. That is why i have created Flask-XXL. Using the 
Flask Factory pattern, specifically one borrowed from "Flask-Kit", that uses a few settings, 
very similar to Django, to automatically do some things for the user, i used to find this 
annoying in Django, it constantly doing things behind my back. Now, i find the freedom inspiring, 
there is so much boilerplate i can now forget about, now i understand what everyone likes about Django. 
But flask is so lightweight and transparent, the source easy to read. But im rambling, so let me show 
you what i mean in the first example. 



##Ch.2 - Getting Started

============================

a typical small flask app might start like this

    from flask import Flask,url_for,redirect,session,g,flash
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return "hello World"
    
    if __name__ == "__main__":
        app.run()
 

but this is obviously a very small example. If you really want a system
that can expand you should start using Blueprints

    from flask import Blueprint
    
    blog = Blueprint('blog',__name__,
           template_folder='templates',
           url_prefix='/blog')
    from .views import *
    
now most tutorials say to keep going like the original 
example

    @blog.route('/')
    def blog():
        return "my blog"
        

but this is where we take our _turn_,

so the first thing to look at in any big web system like this, id say is the settings file, or whichever
config holds the database info. 

here thats <code>settings.py</code> a file that is very similar now to djangos <code>settings.py</code>




##Ch.3 Settings file
                                                        
======================                            
                                                            
the main settings here are              
                                #Django Equivilants
                                #++++++++++++++++++++
    INSTALLED_BLUEPRINTS = [    #<-- INSTALLED_APPS
            XXXXX
    ]
    TEMPLATE_FILTERS = [   [    #<-- Django dosent have a setting for this feature,  just a clunky api
            XXXXXX
    ]
    CONTEXT_PROCESSORS = [      #<-- TEMPLATE_CONTEXT_PROCESSORS
            XXXXXXX
    ]
    ROUTE_MODULES = [           #<-- ROOT_URLCONF
            XXXXXX
    ]
    TEMPLATE_LOADERS = [        #<-- TEMPLATE_LOADERS
            xxxxxx
    ]
    EXTRA_TEMPLATE_DIRS = [     #<-- TEMPLATE_DIRS
            xxxxxxxx
    ]


These 4 settings handle many things that normally take quite some time to get right, 
and boils them down to a few easy processes. 

###INSTALLED_BLUEPRINTS

+++++++++++++++++++++++

this takes the place of Djangos <code>INSTALLED_APPS</code> but for flask blueprints.
It works the same way. just add the import path of a Blueprint, it can be anywhere,
even in a seperate installed package, as long as its importable on your PYTHONPATH.
Heres a an example of the setting

    INSTALLED_BLUEPRINTS = [
                'flask.ext.xxl.apps.auth.auth', #these are a few of the blueprints 
                'flask.ext.xxl.apps.page.page', #built into flask-xxl
                'admin.admin', # these are blueprints inside the webapp
                'blog.blog'
     ]
 
###TEMPLATE_FILTERS

+++++++++++++++++++  

now in Django you can write and register your own template filters,
but i think its kind of a hassle. Flask has an easy way to do it that ive always 
loved, but this makes it much eaiser.

1. step1 - write the filter heres an example that will pull all of the x's from the input and return the result
    

    
        def filter_out_xs(data):
            rtn = ''
            for char in data:
                if char.lower() == 'x':
                    pass
                else:
                    rtn += char
            return rtn


2. step2 just add to the setting, if it was in myapp.template_filters i would put

     
     
        TEMPLATE_FILTERS = [
            'myapp.template_filters.filter_out_xs',
        ]
        

then it could be used in a template like this:

            {{ someval|filter_out_xs }}
            
and of the input was
> 'xx55x76'

the output would be 
> '5576'
    

###CONTEXT_PROCESSORS

+++++++++++++++++++++


A better way to think of context_processors, is global template variables.
Basicly they are functions you can define, that can return data and objects
into the global template environment. Then those objects or that data, is avialiable 
upon rendering templates. This can be very powerful, and it is just as easy here as it is
in Django.

Heres a simple example:

    def simple_context():
        return dict(somevar='someval')
        
    def extra_func():
        return 'somthing i computed'
        
    def complicated_context():
        return dict(complicated=extra_func)
        

now this is in myapp/context_processors.py in the settings file id put

    CONTEXT_PROCESSORS = [
        'myapp.context_processors.simple_context',
        'myapp.context_processors.complicated_context',
    ]
    
then in my templates <code>somevar</code> and <code>extra_func</code> would be avialible





##Ch. 4 Flask, Python.. and MTV

--------------------------------


Now most people, well at least most programmers, know about the MVC or Model, View, Controller pattern. In
Python things tend to work a little differently, first lets look at the traditional __MVC__ pattern.

* a model class mapping database tables to objects and associcated data within the program
    * M
* a few view classes (with related latout,block or template files/classes) to process that data for display
    * V
* finally You would normally have a some kind of front controller class that routes http requests to the views
    * C


now python dosent handle the http requests as cleanly as some languages might, and as a consiquense of that
the routing mainly happens behind the scenes, and is handeled on by the user via either a config style syntax,
or a decoraotor syntax ie:

config style:


    routes = (
        ((Bp),
        ('/',AView.as_view('view')),
    )


decorator style:

    @app.route('/')
    def view_func():
        return a_view()



