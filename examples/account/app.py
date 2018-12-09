#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.account
a account example written by torstack

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
from os.path import abspath, dirname
from torstack.server import TorStackServer

PROJECT_DIR = dirname(dirname(abspath(__file__)))
CONF_DIR = os.path.join(PROJECT_DIR, '__conf')
CONF_FILE = CONF_DIR + os.path.sep + 'dev.conf'

from tornado.web import url
from handlers import HomeHandler, LoginHandler, RegisterHandler, LogoutHandler
handlers = [
    url(r"/", HomeHandler, name='home'),
    url(r"/login", LoginHandler, name='login'),
    url(r"/register", RegisterHandler, name='register'),
    url(r"/logout", LogoutHandler, name='logout'),
]

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)

    template_path = server.config.get('settings', 'template_path')
    static_path = server.config.get('settings', 'static_path')
    template_path = os.path.join(PROJECT_DIR, template_path)
    static_path = os.path.join(PROJECT_DIR, static_path)
    server.config.set('settings', 'template_path', template_path)
    server.config.set('settings', 'static_path', static_path)

    server.run(handlers)


if __name__ == "__main__":
    main()