#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.helloworld
a helloworld example written by torstack

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
from os.path import abspath, dirname
from torstack.server import TorStackServer
from torstack.handler.base import BaseHandler

PROJECT_DIR = dirname(dirname(abspath(__file__)))
CONF_DIR = os.path.join(PROJECT_DIR, '__conf')
CONF_FILE = CONF_DIR + os.path.sep + 'dev.conf'

class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    server.run([(r"/", MainHandler)])


if __name__ == "__main__":
    main()