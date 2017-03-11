VERSION = '0,9,13'
import os
from setuptools import setup, find_packages,findall
from glob import glob

def get_description():
    return open('README.txt','r').read()

def get_version():
    l,m,s = VERSION.split(',')
    return '{0}.{1}.{2}'.format(l,m,s).strip()

data = os.walk(os.path.dirname(__file__))

make_file = lambda dn,f: os.path.join(os.curdir,os.sep,dn,f)

def get_pkg_data():
    data = os.walk(os.path.abspath(os.curdir))
    pkg_data = []

    for dn,dl,fl in data:
        if 'templates' in dn.split('/'):
            for f in fl:
                if not f.endswith('.py'):
                    pkg_data.append(make_file(dn,f))
    return pkg_data

config = dict(
        name='flask-xxl',
        version=get_version(),#'0.0.9',
        include_package_data=True,
        author='Kyle Roux',
        author_email='kyle@level2designs.com',
        description='quick way to design large flask projects',
        long_description=get_description(),
        packages=['flask_xxl'],
        package_data = {'':findall('flask_xxl')},     #['*.bob','*.html','*.js','*.css','*',]},
        install_requires=[
            'flask==0.10.1',
            'flask-alembic==1.0.2',
            'flask-sqlalchemy==2.0',
            'flask-script==2.0.5',
            'flask-WTF==0.10.2',
            'jinja2==2.7.3',
            'LoginUtils==1.0.1',
            'Mako==1.0.0',
            'MarkupSafe==0.23',
            'SQLAlchemy==0.9.8',
            'WTForms==2.0.1',
            'Werkzeug==0.9.6',
            'alembic==0.6.7',
            'argparse==1.2.1',        
            'itsdangerous==0.24',
            'wsgiref==0.1.2',
            'six==1.8.0',
            'mr.bob2==0.2.3',
            'Flask-DebugToolbar==0.9.2',
            'Flask-PageDown==0.1.5',
            'Pygments==2.0.1',
            'flask-codemirror==0.0.3',
            'jinja2-highlight==0.6.1',
            'requests==2.5.1',
            'inflection==0.2.1',
            'markdown==2.5.2',
            ],
        zip_safe=False,
        entry_points=dict(
            console_scripts='flaskxxl-manage.py=flask_xxl.manage:main'
            ),
)

if __name__ == "__main__":
    setup(**config)
