#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.helloworld
a helloworld example written by torstack

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
from tornado import gen
from os.path import abspath, dirname
from torstack.server import TorStackServer
from torstack.handler.base import BaseHandler

PROJECT_DIR = dirname(dirname(abspath(__file__)))
CONF_DIR = os.path.join(PROJECT_DIR, '__conf')
CONF_FILE = CONF_DIR + os.path.sep + 'helloworld.conf'

class MainHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        self.write("Hello, world")

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    print(server.config._dict)
    server.add_handlers([(r"/", MainHandler)])
    server.run()


if __name__ == "__main__":
    main()