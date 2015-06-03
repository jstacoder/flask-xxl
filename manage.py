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

def main():
    flaskxxl.test_request_context().push() 
    manager.add_command('mrbob',mrbob_manager)
    manager.add_command('clean',Clean())
    manager.add_command('urls',ShowUrls())
    manager.run(default_command='mrbob')

if __name__ == '__main__':
    main()
