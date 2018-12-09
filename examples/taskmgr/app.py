#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.helloworld.app.py
helloworld app.py definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
import sys
from os.path import abspath, dirname
from torstack.server import TorStackServer
from torstack.handler.base import BaseHandler
sys.path.append('..')

PROJECT_DIR = dirname(dirname(abspath(__file__)))
CONF_DIR = os.path.join(PROJECT_DIR, '__conf')
CONF_FILE = CONF_DIR + os.path.sep + 'dev.conf'

from executer import TestExecuter
print(TestExecuter.id)

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, taskmgr")

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    server.config.set('scheduler', 'enable', True)
    server.config.set('scheduler', 'autorun', True)
    server.config.add_executers([TestExecuter])

    server.run([(r"/", MainHandler)])


if __name__ == "__main__":
    main()