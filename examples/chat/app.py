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

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(PROJECT_PATH, '__conf')
CONF_FILE = os.path.join(CONF_PATH, 'chat.conf')
sys.path.insert(0,PROJECT_PATH)

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
    server.config.load(CONF_FILE)
    server.config._dict['application']['project_path'] = PROJECT_PATH
    server.config._dict['application']['settings']['template_path'] = '%s%s' % (PROJECT_PATH, server.config._dict['application']['settings']['template_path'])
    server.config._dict['application']['settings']['static_path'] = '%s%s' % (PROJECT_PATH, server.config._dict['application']['settings']['static_path'])
    server.add_handlers(handlers)
    server.init_application()
    server.add_websocket('channel')
    server.run(8888)


if __name__ == "__main__":
    main()