VERSION = '0,4,5'
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
    def find_packages():
        return ['flask-xxl']

def get_description():
    return open('README.txt','r').read()

def get_version():
    l,m,s = VERSION.split(',')
    return '{}.{}.{}'.format(l,m,s).strip()

config = dict(
        name='flask-xxl',
        version=get_version(),#'0.0.9',
        include_package_data=True,
        package_data = {
            '':['*.md','*.txt']
        },
        author='Kyle Roux',
        author_email='kyle@level2designs.com',
        description='quick way to design large flask projects',
        long_description=get_description(),
        packages=find_packages(),
        package_dir={'':'.'},
        install_requires=['LoginUtils'],
        entry_points=dict(
            console_scripts='flaskxxl-manage.py=flask_xxl.manage:main'
            )
)

setup(**config)
