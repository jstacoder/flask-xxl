from flask.ext.script import Manager,prompt
from flask.ext.script.commands import Clean,ShowUrls
from flask_xxl import flaskxxl
import os


manager = Manager(flaskxxl)



@manager.command
def mk_dir():
    dirname = prompt('What dir to make',None)
    if dirname is not None and dirname != ' ':
        if not os.path.exists(dirname):
            os.mkdir(dirname)

if __name__ == "__main__":
    manager.add_command('show_urls',ShowUrls())
    manager.add_command('clean',Clean())
    manager.run()
