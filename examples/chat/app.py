#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.chat
a chat example written by torstack

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
import sys
from tornado.web import url
from torstack.server import TorStackServer

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_DIR = os.path.join(PROJECT_DIR, '__conf')
CONF_FILE = CONF_DIR + os.path.sep + 'dev.conf'
sys.path.insert(0,PROJECT_DIR)

from chat.handlers import HomeHandler, WebSocketHandler
from account.handlers import LoginHandler, RegisterHandler, LogoutHandler
handlers = [
    url(r"/", HomeHandler, name='home'),
    url(r"/login", LoginHandler, name='login'),
    url(r"/register", RegisterHandler, name='register'),
    url(r"/logout", LogoutHandler, name='logout'),
    url(r'/ws', WebSocketHandler, name='ws'),
]

def main():
    server = TorStackServer()
    server.load_config(CONF_FILE)

    template_path = server.config['settings']['template_path']
    static_path = server.config['settings']['static_path']
    server.config['settings']['template_path'] = os.path.join(PROJECT_DIR, template_path)
    server.config['settings']['static_path'] = os.path.join(PROJECT_DIR, static_path)
    server.config['websocket']['enable'] = True

    server.load_handlers(handlers)
    server.run()


if __name__ == "__main__":
    main()