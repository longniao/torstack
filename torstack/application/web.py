# -*- coding: utf-8 -*-

'''
torstack.application.application
Basic application definition.

:copyright: (c) 2018 by longniao <longniao@gmail.com>
:license: MIT, see LICENSE for more details.
'''

import importlib
import sys

importlib.reload(sys)
from torstack.exception import BaseException
import tornado.httpserver
import tornado.web
from tornado.options import options
from torstack.config.default import *


class WebApplication(tornado.web.Application):

    settings = {}

    def __init__(self):

        if hasattr(options, '_CONFIG_DICT_'):
            config = options._CONFIG_DICT_
        else:
            raise BaseException('10001', 'error config.')

        # application
        if 'application' not in config:
            raise BaseException('10002', 'error application config.')

        # application settings
        self.settings = {**application_config, **config['application']}

        # redis
        if 'redis' in config:
            from torstack.storage.redis import RedisStorage
            redis_storage = RedisStorage(config['redis'])
            self.settings['_storage_redis'] = redis_storage

        # mysql
        if 'mysql' in config:
            from torstack.storage.mysql import MysqlStorage
            mysql_storage = MysqlStorage(config['mysql'])
            self.settings['_storage_mysql'] = mysql_storage

        # mongodb
        if 'mongodb' in config:
            pass

        # memcache
        if 'memcache' in config:
            pass

        # session
        if 'session' in config:
            self.settings['_config_session'] = {**session_config, **config['session']}

        # cookie
        if 'cookie' in config:
            self.settings['_config_cookie'] = {**cookie_config, **config['cookie']}

        # base
        if 'base' in config:
            self.settings['_config_base'] = {**base_config, **config['base']}

    def run(self, handlers):
        '''
        run application
        :param handlers:
        :return:
        '''
        if not handlers:
            raise BaseException('10003', 'error application handlers.')

        tornado.web.Application.__init__(self, handlers, **self.settings)