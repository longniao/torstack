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


class RestApplication(tornado.web.Application):

    settings = {}

    def __init__(self):

        if hasattr(options, '_CONFIG_DICT_'):
            config = options._CONFIG_DICT_
        else:
            raise BaseException('10001', 'error config.')

        # ===================================================================
        # ======= config ====================================================
        # ===================================================================

        # application
        if 'application' not in config:
            raise BaseException('10002', 'error application config.')

        # application settings
        self.settings = application_config.update(config['application'])

        # base
        if 'base' in config:
            self.settings['_config_base'] = base_config.update(config['base'])

        # rest config
        rest_config = dict(
            allow_remote_access=True,
        )
        if 'rest' in config:
            rest_config.update(cookie_config.update(config['rest']))
            self.settings['_config_rest'] = rest_config

        # token config
        if 'token' in config:
            self.settings['_config_token'] = cookie_config.update(config['token'])

        # ===================================================================
        # ======= storage ===================================================
        # ===================================================================

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

        # ===================================================================
        # ======= session and cookie ========================================
        # ===================================================================

        # token
        from torstack.core.token import CoreToken
        self.settings['token'] = CoreToken(redis_storage, self.settings['_config_token'])


    def run(self, handlers):
        '''
        run application
        :param handlers:
        :return:
        '''
        if not handlers:
            raise BaseException('10003', 'error application handlers.')

        tornado.web.Application.__init__(self, handlers, **self.settings)