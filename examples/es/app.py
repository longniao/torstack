#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.helloworld
a helloworld example written by torstack

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import sys
import os
from torstack.server import TorStackServer

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(PROJECT_PATH, '__conf')
CONF_FILE = CONF_PATH + os.path.sep + 'es.conf'
sys.path.insert(0,PROJECT_PATH)

from es.handlers import MainHandler

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    print(server.config._dict)
    server.add_handlers([(r"/", MainHandler)])
    server.init_application()
    server.run()

if __name__ == "__main__":
    main()