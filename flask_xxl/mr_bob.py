from flask.ext.script import Manager, prompt_bool
import os
from mrbob import cli 
import sys

manager = Manager(usage="performs mr.bob template runs")

EXT_ROOT = os.path.abspath(os.path.dirname(__file__))

MRBOB_TEMPLATE_DIR = os.path.join(EXT_ROOT,'templates')


def get_all_files(dirname):
    rtn = []
    for dname,dlist,flist in os.walk(dirname):
        for itm in flist:
            rtn.append(os.path.join(dname,itm))
        if len(dlist) == 0:
            return rtn
        else:
            for d in dlist:
                rtn.append(get_all_files(d))


def get_templates():
    return os.listdir(MRBOB_TEMPLATE_DIR)

@manager.command
def print_template_dir():
    print MRBOB_TEMPLATE_DIR

@manager.command
def print_templates():
    print ', '.join(map(str,get_templates()))

@manager.option('template',nargs='?',default=None)
def print_template_files(template):
    if template is None:
        print ''
        return
    else:
        if not template in get_templates():
            print 'Error! {} is not installed'.format(template)
            return
    #print ''.join(map(str,['{},\n'.format(itm) for itm in os.listdir(os.path.join(MRBOB_TEMPLATE_DIR,template))]))
    print '\n'.join(map(str,[str(x) for x in get_all_files(os.path.join(MRBOB_TEMPLATE_DIR,template)) if not x is None]))
    
@manager.option("-t","--testing",action='store_true')
def start_project(testing=False):
    template_dir = os.path.join(MRBOB_TEMPLATE_DIR,'project')
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

@manager.option("-t","--testing",action="store_true")
def add_blueprint(testing=False):
    template_dir = os.path.join(MRBOB_TEMPLATE_DIR,'blueprint')
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

   




