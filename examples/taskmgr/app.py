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
from torstack.server import TorStackServer
from torstack.handler.base import BaseHandler
sys.path.append('..')

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(PROJECT_PATH, '__conf')
CONF_FILE = os.path.join(CONF_PATH, 'taskmgr.conf')

from executer import TestExecuter

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, taskmgr")

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    server.add_executers([TestExecuter])
    server.add_handlers([(r"/", MainHandler)])
    server.init_application()
    server.run()


if __name__ == "__main__":
    main()