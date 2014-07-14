try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def get_description():
    return open('README.md','r').read()

def get_version():
    l,m,s = open('version','r').read().split(',')
    return '{}.{}.{}'.format(l,m,s)

config = dict(
        name='flask-xxl',
        version=get_version(),
        include_package_data=True,
        author='Kyle Roux',
        author_email='kyle@level2designs.com',
        description='quick way to design large flask projects',
        long_description=get_description()
)

setup(**config)
