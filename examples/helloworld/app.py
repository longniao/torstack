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
from tornado.options import define, options
from configparser import ConfigParser
import ast
from torstack.server import TorStackServer
from torstack.handler.base import BaseHandler

PROJECT_DIR = dirname(dirname(abspath(__file__)))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'website/template')
STATIC_DIR = os.path.join(PROJECT_DIR, 'website/static')
CONF_DIR = os.path.join(PROJECT_DIR, 'conf')
CONF_FILE = CONF_DIR + os.path.sep + 'dev.conf'

print('PROJECT_DIR:', PROJECT_DIR)
print('TEMPLATE_DIR:', TEMPLATE_DIR)
print('STATIC_DIR:', STATIC_DIR)
print('CONF_DIR:', CONF_DIR)
print('CONF_FILE:', CONF_FILE)

config = ConfigParser()
config.read(CONF_FILE, encoding='UTF-8')
settings = ast.literal_eval(config.get('application', 'settings'))
log = ast.literal_eval(config.get('application', 'log'))
redis = ast.literal_eval(config.get('redis', 'master'))
mysql = dict(
    master=ast.literal_eval(config.get('mysql', 'master')),
    slave=ast.literal_eval(config.get('mysql', 'slave')),
)
session = ast.literal_eval(config.get('base', 'session'))
cookie = ast.literal_eval(config.get('base', 'cookie'))

settings['template_path'] = TEMPLATE_DIR
settings['static_path'] = STATIC_DIR

_CONFIG_DICT_ = dict(
    application=settings,
    session=session,
    cookie=cookie,
    log=log,
    redis=redis,
    mysql=mysql,
)

define("_CONFIG_DICT_", default=_CONFIG_DICT_, type=dict)

print('_CONFIG_DICT_:', _CONFIG_DICT_)



class MainHandler(BaseHandler):
    def get(self):
        self.write("Hello, world")


def main():
    server = TorStackServer()
    server.run([(r"/", MainHandler)])


if __name__ == "__main__":
    main()