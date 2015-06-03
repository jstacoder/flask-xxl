from flask.ext.script import Manager, prompt_bool
import os
from mrbob import cli
import mrbob
from jinja2.loaders import FileSystemLoader
import sys


manager = Manager(usage="performs mr.bob template runs")

EXT_ROOT = os.path.abspath(os.path.dirname(__file__))

MRBOB_TEMPLATE_DIR = os.path.join(EXT_ROOT,'templates')
mrbob.rendering.jinja2_env.loader = FileSystemLoader(MRBOB_TEMPLATE_DIR)


def get_all_files(dirname,seen=None):
    rtn = set()
    if seen is None:
        seen = set()
    seen.add(dirname)
    for dname,dlist,flist in os.walk(dirname):
        for itm in flist:
            if not itm.endswith('.pyc'):
                rtn.add(os.path.join(dname,itm))
        if len(dlist) == 0:
            return rtn
        else:
            for d in dlist:
                pth = os.path.join(dname,d)
                if not pth in seen:
                    rtn.update(get_all_files(pth,seen))

remove_dir = lambda dirname,path: path.split(dirname)[-1]
remove_bob = lambda x: x.replace('.bob','')


def get_templates():
    return [name for name in os.listdir(MRBOB_TEMPLATE_DIR) if not name.startswith('_') and not name.endswith('.pyc')]

@manager.command
def print_template_dir():
    print MRBOB_TEMPLATE_DIR

@manager.command
def print_templates():
    print ', '.join(map(str,get_templates()))

@manager.option('template',nargs='?',default=None)
def print_template_files(template=None):
    if template is None:
        print 'please provide a template name'
        return
    else:
        if not template in get_templates():
            print 'Error! {} is not installed'.format(template)
            return
    print '\n'.join(
                    map(
                        str,
                            [remove_bob(remove_dir(
                                MRBOB_TEMPLATE_DIR,x
                        )) for x in get_all_files(
                                            os.path.join(
                                                    MRBOB_TEMPLATE_DIR,template
                                            )
                        ) if not x is None and not x.endswith('.pyc')
                             ]
                        )
    )
_template_dir = lambda name: os.path.join(MRBOB_TEMPLATE_DIR,name)
    
@manager.option("-t","--testing",action='store_true')
def start_project(testing=False):
    template_dir = _template_dir('project')
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
    template_dir = _template_dir('blueprint')
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
def angular_app():
    template_dir = _template_dir('angular_app')
    target_dir = os.path.join(os.curdir,'static','js')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    list_questions = False
    non_interactive = False
    args = [template_dir,'-O',target_dir,'-v','-w']
    cli.main(args)

@manager.command
def angular_service():
    template_dir = _template_dir('angular_service')
    target_dir = os.path.join(os.curdir,'static','js')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    list_questions = False
    non_interactive = False
    args = [template_dir,'-O',target_dir,'-v','-w']
    cli.main(args)





