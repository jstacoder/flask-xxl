from flask.ext.script import prompt_bool
from manage import manager
from mrbob import cli
import sys
import os
from flask_xxl import flaskxxl



def get_template_dir():
    EXT_ROOT = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(EXT_ROOT,'templates')


def print_usage():
    print 'flaskxxl-manage.py [start-project] [start-blueprint]'

def run_mrbob(template_dir,testing):
    if testing:
        target_dir = './testing'
    else:
        target_dir = os.curdir
    if target_dir == os.curdir:
        if not prompt_bool('not testing, are you sure you want to continue...'):
            sys.exit(0)
    list_questions = False
    non_interactive = False
    args = [template_dir,'-O',target_dir,'-v','-w']
    cli.main(args)


@manager.command
def start_blueprint(testing=False):
    template_dir = os.path.join(get_template_dir(),'blueprint')
    run_mrbob(template_dir,testing)




@manager.command
def start_project(testing=False):
    template_dir = os.path.join(get_template_dir(),'project')
    run_mrbob(template_dir,testing)


def main():
    func = None
    testing = False
    if len(sys.argv) <= 1:
        print_usage()
    else:
        if sys.argv[1] == 'start-project':
            func = start_project
        elif sys.argv[1] == 'start-blueprint':
            func = start_blueprint
        else:
            print_usage()
            sys.exit()
        if len(sys.argv) > 2:
            if sys.argv[2] == '-t' or sys.argv[2] == '--testing':
                testing = True
            else:
                testing = False
        if func is not None:
            func(testing)

if __name__ == "__main__":
    with flaskxxl.context() as ctx:
        manager.run()
