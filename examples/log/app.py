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
import logging

logger = logging.getLogger(__name__)
error_logger = logging.getLogger('error')
collect_logger = logging.getLogger('collect')

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(PROJECT_PATH, '__conf')
CONF_FILE = CONF_PATH + os.path.sep + 'log.conf'

class MainHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        logger.debug('debug 信息')
        logger.info('info 信息')
        logger.warning('warning 信息')
        logger.error('error 信息')
        logger.critical('critial 信息')

        error_logger.debug('debug 信息')
        error_logger.info('info 信息')
        error_logger.warning('warning 信息')
        error_logger.error('error 信息')
        error_logger.critical('critial 信息')

        collect_logger.debug('debug 信息')
        collect_logger.info('info 信息')
        collect_logger.warning('warning 信息')
        collect_logger.error('error 信息')
        collect_logger.critical('critial 信息')
        self.write("Hello, world")

def main():
    server = TorStackServer()
    server.config.load(CONF_FILE)
    server.add_handlers([(r"/", MainHandler)])
    # server.init_application()
    server.run()

if __name__ == "__main__":
    main()