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
from torstack.server import TorStackServer
from torstack.handler.base import BaseHandler

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(PROJECT_PATH, '__conf')
CONF_FILE = CONF_PATH + os.path.sep + 'memcache.conf'

class MainHandler(BaseHandler):

    def initialize(self):
        super(MainHandler, self).initialize()
        self.memcache = self.storage['memcache']

    @gen.coroutine
    def get(self):
        self.memcache.save('key', 'Hello, memcache')
        msg = self.memcache.get('key')
        print(msg, type(msg))
        self.write(msg)

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    server.add_handlers([(r"/", MainHandler)])
    server.init_application()
    server.run()

if __name__ == "__main__":
    main()