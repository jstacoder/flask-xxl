#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    manage
    ~~~~~~
"""
import subprocess
from flask.ext.script import Shell, Manager, prompt_bool
from flask.ext.script.commands import Clean,ShowUrls
from flask.ext.xxl import flaskxxl
manager = Manager(flaskxxl)
from flask.ext.xxl.mr_bob import manager as mrbob_manager
import sys

def main(auto=False):
    if not auto:
        sys.argv.insert(1,'mrbob')
    flaskxxl.test_request_context().push() 
    manager.add_command('mrbob',mrbob_manager)
    manager.add_command('clean',Clean())
    manager.add_command('urls',ShowUrls())
    default_cmd = 'mrbob'
    if len(sys.argv) > 2:
        default_cmd = 'clean'
    manager.run(default_command=default_cmd)

if __name__ == '__main__':
    main(auto=True)
