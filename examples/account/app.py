#!/usr/bin/env python
#  -*- coding: utf-8 -*-

'''
torstack.examples.helloworld.app.py
helloworld app.py definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import os
from os.path import abspath, dirname
from torstack.config.container import ConfigContainer
from torstack.server import TorStackServer

PROJECT_DIR = dirname(dirname(abspath(__file__)))
CONF_DIR = os.path.join(PROJECT_DIR, '__conf')
CONF_FILE = CONF_DIR + os.path.sep + 'dev.conf'

ConfigContainer.load_config(CONF_FILE)
ConfigContainer.store()

template_path = ConfigContainer.get('settings', 'template_path')
static_path = ConfigContainer.get('settings', 'static_path')

template_path = os.path.join(PROJECT_DIR, template_path)
static_path = os.path.join(PROJECT_DIR, static_path)

ConfigContainer.set('settings', 'template_path', template_path)
ConfigContainer.set('settings', 'static_path', static_path)

from tornado.web import url
from handlers import HomeHandler, LoginHandler, RegisterHandler
handlers = [
    url(r"/", HomeHandler, name='home'),
    url(r"/login", LoginHandler, name='login'),
    url(r"/register", RegisterHandler, name='register'),
    url(r"/reset", LoginHandler, name='reset'),
]

def main():
    server = TorStackServer()
    server.run(handlers)


if __name__ == "__main__":
    main()