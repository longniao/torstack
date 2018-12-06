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

ConfigContainer.set('scheduler', 'enable', True)
ConfigContainer.set('scheduler', 'autorun', True)
print(ConfigContainer.get_config())

handlers = []

def main():
    server = TorStackServer()
    server.run(handlers)


if __name__ == "__main__":
    main()