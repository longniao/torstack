#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.account
a account example written by torstack

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
import sys
from tornado.web import url
from torstack.server import TorStackServer

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(PROJECT_PATH, '__conf')
CONF_FILE = os.path.join(CONF_PATH, 'restful.conf')
sys.path.insert(0,PROJECT_PATH)

from restful.handlers import InitHandler, ErrorHandler
handlers = [
    url(r"/", InitHandler, name='init'),
    url(r"/(.*)", ErrorHandler, name='error'),
]

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    server.add_handlers(handlers)
    server.init_application()
    server.run()

if __name__ == "__main__":
    main()