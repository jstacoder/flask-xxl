from flask.ext.script import Manager, prompt_bool
import os
from mrbob import cli 
import sys

manager = Manager(usage="performs mr.bob template runs")

EXT_ROOT = os.path.abspath(os.path.dirname(__file__))

MRBOB_TEMPLATE_DIR = os.path.join(EXT_ROOT,'templates')


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

   




